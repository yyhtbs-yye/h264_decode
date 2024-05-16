import cv2
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed

def process_image(subdir, img_name, input_folder, output_folder_video, output_folder_image, output_folder_xml):

    # Construct full image path
    img_path = os.path.join(input_folder, subdir, img_name)
    temp_video_path = os.path.join(output_folder_video, subdir, img_name[:-4] + ".mp4")
    output_image_path = os.path.join(output_folder_image, subdir, img_name)
    temp_264_path = os.path.join(output_folder_video, subdir, img_name[:-4] + ".264")
    output_xml_path = os.path.join(output_folder_xml, subdir, img_name[:-4] + ".yuv")
    xml_trace_path = os.path.join(output_folder_xml, subdir, img_name[:-4] + "_trace.xml")
    
    # Step 1: Encode the image into an I-frame using ffmpeg
    subprocess.run([
        '/usr/bin/ffmpeg',
        '-y',  # Overwrite output files without asking
        '-loop', '1',  # Loop over the input image
        '-i', img_path,  # Input file
        '-c:v', 'libx264',  # Specify the codec: H.264
        '-t', '0.1',  # Set the duration of the output video
        '-pix_fmt', 'yuv420p',  # Set pixel format
        '-vf', 'scale=iw/4:4ih/4',  # Ensure dimensions are even
        '-frames:v', '1',  # Only one video frame
        temp_video_path  # Temporary output video path
    ])
    
    # Step 2: Read the video frame using OpenCV and save it as a PNG
    cap = cv2.VideoCapture(temp_video_path)
    
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            # Save the frame as a PNG image
            cv2.imwrite(output_image_path, frame)
        else:
            print(f"Could not read the frame from {temp_video_path}")
    else:
        print(f"Failed to open the video {temp_video_path}")
    
    cap.release()
    
    # Step 3: Convert .mp4 to .264 using ffmpeg
    subprocess.run([
        '/usr/bin/ffmpeg',
        '-y',  # Overwrite output files without asking
        '-i', temp_video_path,  # Input file
        '-vcodec', 'copy',  # Copy the video codec
        '-an',  # No audio
        '-bsf:v', 'h264_mp4toannexb',  # Bitstream filter for H.264
        temp_264_path  # Output .264 file
    ])
    
    # Step 4: Decode .264 to .yuv using ldecod
    subprocess.run([
        './jm_16.1/bin/ldecod.exe',
        '-i', temp_264_path,  # Input .264 file
        '-o', output_xml_path,  # Output .yuv file
        '-xmltrace', xml_trace_path  # XML trace file
    ])

def encode_images_to_iframe(input_folder, output_folder_video, output_folder_image, output_folder_xml):
    # Check if the output folders exist, if not, create them
    if not os.path.exists(output_folder_video):
        os.makedirs(output_folder_video)
    if not os.path.exists(output_folder_image):
        os.makedirs(output_folder_image)
    if not os.path.exists(output_folder_xml):
        os.makedirs(output_folder_xml)

    # Iterate over all subfolders in the input folder
    for subdir in os.listdir(input_folder):
        subfolder_path = os.path.join(input_folder, subdir)
        
        # Check if it's a directory
        if os.path.isdir(subfolder_path):
            # Collect all PNG images in the subfolder
            images = [img_name for img_name in os.listdir(subfolder_path) if img_name.lower().endswith('.png')]

            # Check and create output directories if they don't exist
            if not os.path.exists(os.path.join(output_folder_video, subdir)):
                os.makedirs(os.path.join(output_folder_video, subdir))

            if not os.path.exists(os.path.join(output_folder_image, subdir)):
                os.makedirs(os.path.join(output_folder_image, subdir))

            if not os.path.exists(os.path.join(output_folder_xml, subdir)):
                os.makedirs(os.path.join(output_folder_xml, subdir))

            # Process each image in the subfolder in parallel
            with ThreadPoolExecutor() as executor:
                futures = [executor.submit(process_image, subdir, img_name, input_folder, output_folder_video, output_folder_image, output_folder_xml) for img_name in images]
                for future in as_completed(futures):
                    future.result()  # If there's any exception, it will be raised here

# Example usage
input_folder = 'datasets/REDS/train_sharp'  # Replace with your input directory
output_folder_video = 'datasets/REDS/train_h264_intra_only_video'  # Replace with your desired output directory
output_folder_image = 'datasets/REDS/train_h264_intra_only'  # Replace with your desired output directory
output_folder_xml = 'datasets/REDS/train_h264_intra_only_xml'  # Replace with your desired output directory

encode_images_to_iframe(input_folder, output_folder_video, output_folder_image, output_folder_xml)
