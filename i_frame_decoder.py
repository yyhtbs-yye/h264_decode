import numpy as np
from scipy.fftpack import idct
import matplotlib.pyplot as plt
import xmltodict

# Default 4x4 quantization matrix for intra-frame coefficients
DEFAULT_4x4_QUANT_MATRIX = np.array([
    [16, 11, 10, 16],
    [12, 12, 14, 19],
    [14, 13, 16, 24],
    [14, 17, 22, 29]
], dtype=np.uint16)

# Function to apply Inverse Discrete Cosine Transform (IDCT) to a 16x16 block by processing 4x4 sub-blocks
def apply_idct_16x16(block):
    result = np.zeros((16, 16))
    for i in range(0, 16, 4):
        for j in range(0, 16, 4):
            sub_block = block[i:i+4, j:j+4]
            result[i:i+4, j:j+4] = idct(idct(sub_block, axis=0, norm='ortho'), axis=1, norm='ortho')
    return result

# Function to inverse quantize a block
def inverse_quantize(block, q_scale):
    quant_matrix = np.full(block.shape, q_scale, dtype=np.float64)
    return block * quant_matrix

# Scaling factor based on quantization parameter (QP)
QP_SCALE_CR = {
    0: [13107, 5243, 8066],
    1: [11916, 4660, 7490],
    2: [10082, 4194, 6554],
    3: [9362, 3647, 5825],
    4: [8192, 3355, 5243],
    5: [7282, 2893, 4559]
}

def get_q_scale(qp):
    q_bits = 15 + (qp // 6)
    return QP_SCALE_CR[qp % 6][0] >> (q_bits - 15)

# Function to predict the 16x16 block based on the mode and position
def predict_16x16_block(mb_x, mb_y, mode, block_size, residue):
    predicted_block = np.zeros((block_size, block_size))
    
    if mode == '0':
        for col in range(block_size):
            predicted_block[:, col] = residue[mb_y - 1, mb_x + col] if mb_y > 0 else 0
    elif mode == '1':
        for row in range(block_size):
            predicted_block[row, :] = residue[mb_y + row, mb_x - 1] if mb_x > 0 else 0
    elif mode == '2':
        top_mean = np.mean(residue[mb_y - 1, mb_x:mb_x + block_size]) if mb_y > 0 else 0
        left_mean = np.mean(residue[mb_y:mb_y + block_size, mb_x - 1]) if mb_x > 0 else 0
        dc_value = (top_mean + left_mean) / 2
        predicted_block.fill(dc_value)
    elif mode == '3':
        for i in range(block_size):
            for j in range(block_size):
                if mb_y - 1 + i < 0 or mb_x + 1 + j >= residue.shape[1]:
                    predicted_block[i, j] = 0
                else:
                    predicted_block[i, j] = residue[mb_y - 1 + i, mb_x + 1 + j]
    return predicted_block

def generate_luma_channel_from_iframe(frame_xml, frame_width, frame_height, frame_id=None, intra_prediction=True):

    def get_digit_bitmap(digit):
        if digit == '8':
            return 1-np.array([[1, 1, 1],
                             [1, 0, 1],
                             [1, 1, 1],
                             [1, 0, 1],
                             [1, 1, 1]])
        elif digit == '4':
            return 1-np.array([[1, 0, 1],
                             [1, 0, 1],
                             [1, 1, 1],
                             [0, 0, 1],
                             [0, 0, 1]])
        else:
            return np.zeros((5, 3))

    # Initialize full-frame residue arrays for Y
    residue_Y = np.zeros((frame_height, frame_width))

    annotation = np.zeros((frame_height, frame_width))

    for i, mb in enumerate(frame_xml['SubPicture']['Slice']['MacroBlock']):
        mb_x = int(mb['Position']['X'])
        mb_y = int(mb['Position']['Y'])
        qp_y = int(mb['QP_Y'])

        elms = mb['TypeString'].split("_")

        sb_size = elms[1]

        if len(elms) > 2:      # In the case of 4x4 and 8x8
            luma_mode = elms[2]
        else:
            luma_mode = '2'     # Mean DC Mode if Unknown
        
        q_scale = get_q_scale(qp_y)

        coeffs_Y = np.array([int(num) for row in mb['Coeffs']['Plane'][0]['Row'] for num in row.split(',')]).reshape(16, 16)
        
        # Inverse quantization
        block_Y = inverse_quantize(coeffs_Y, q_scale)

        # IDCT
        residue_block_Y = apply_idct_16x16(block_Y)

        # Intra-frame prediction
        predicted_Y = predict_16x16_block(mb_x, mb_y, luma_mode, 16, residue_Y)
        
        if intra_prediction:
            # Add the predicted block to the de-quantized block to get the residual values
            residue_block_Y += predicted_Y
        
        annotation_block = np.ones_like(residue_block_Y)
        
        # Determine the center position for the 5x3 bitmap
        top_left_y = 6  # 16//2 - 5//2
        top_left_x = 7  # 16//2 - 3//2

        if sb_size == "8x8":
            # Embed the bitmap for '8'
            digit_bitmap = get_digit_bitmap('8')
            annotation_block[top_left_y:top_left_y+5, top_left_x:top_left_x+3] = digit_bitmap   # Scale the bitmap
        elif sb_size == "4x4":
            # Embed the bitmap for '4'
            digit_bitmap = get_digit_bitmap('4')
            annotation_block[top_left_y:top_left_y+5, top_left_x:top_left_x+3] = digit_bitmap  # Scale the bitmap

        annotation[mb_y:mb_y+16, mb_x:mb_x+16] = annotation_block
        # Place in the full-frame residue array
        residue_Y[mb_y:mb_y+16, mb_x:mb_x+16] = residue_block_Y

    # Normalize the residue values to the range 0-255 for visualization
    residue_Y_normalized = residue_Y - np.min(residue_Y)
    residue_Y_normalized = residue_Y_normalized / np.max(residue_Y_normalized) * 255
    residue_Y_normalized = residue_Y_normalized.astype(np.uint8)

    return residue_Y_normalized * annotation

if __name__=="__main__":
    xml_file_path = "meerkat_CIF_trace.xml"
    luma_output = generate_luma_channel_from_iframe(xml_file_path)

    # Plot the normalized residue
    plt.figure(figsize=(10, 8))
    plt.imshow(luma_output, cmap='gray', interpolation='nearest')
    plt.colorbar()
    plt.title('Residue Y Visualization')
    plt.show()
