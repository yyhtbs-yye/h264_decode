# This is step 2 to convert h264 file (*.mp4) to h264 bitstream files (*.264). 
# IN PATH@REDS_H264_OUTPUT/
# 000.mp4
# 001.mp4
# ...
# 169.mp4

import subprocess
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Directory containing the images

def save_h264_to_bitstream(input_base_dir, video_name, output_base_dir):

    subprocess.run([
        '/usr/bin/ffmpeg',
        '-y',                                       # Overwrite output files without asking
        '-i', os.path.join(input_base_dir, 
                           video_name + ".mp4"),    # Input file
        '-vcodec', 'copy',                          # Copy the video codec
        '-an',                                      # No audio
        '-bsf:v', 'h264_mp4toannexb',               # Bitstream filter for H.264
        os.path.join(output_base_dir, 
                     video_name + ".264")           # Output .264 file
    ])


if __name__=="__main__":

    input_base_dir = "REDS_H264_OUTPUT"    # Update this with the path to your images
    output_base_dir = "REDS_264_bitstream_OUTPUT"            # Path for the output video

    os.system(f"rm {output_base_dir}/*")

    if not os.path.exists(output_base_dir):
        os.makedirs(output_base_dir)

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(save_h264_to_bitstream, 
                                   input_base_dir, video_name[:-4], output_base_dir) 
                    for video_name in os.listdir(input_base_dir)]
        for future in as_completed(futures):
            future.result()  # If there's any exception, it will be raised here

        
