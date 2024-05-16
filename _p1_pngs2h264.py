# This is step 1 to convert Image files (*.png) to h264 file (*.mp4). 
# IN PATH@datasets/REDS/train_sharp/
# 000/00000000.png - 000/00000099.png
# 001/00000000.png - 001/00000099.png
# ...
# 169/00000000.png - 169/00000099.png

import subprocess
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Directory containing the images

def merge_images_to_h264(input_base_dir, video_name, output_base_dir):

    # Execute the ffmpeg command to merge images into a video
    subprocess.run([
        '/usr/bin/ffmpeg',
        '-y',  # Overwrite output files without asking
        '-framerate', '24',  # Frame rate (frames per second)
        '-i', f'{input_base_dir}/{video_name}/%08d.png',  # Input files format
        '-frames:v', '15',  # Process only 15 frames
        '-c:v', 'libx264',                  # Video codec
        # '-bf', '0',                         # Force no B frames
        '-partitions', 'none',
        '-x264-params', 'keyint=1:min-keyint=1',  # Force every frame to be a key frame (I-frame)
        '-pix_fmt', 'yuv420p',              # Pixel format
        '-vf', 'scale=iw/4:ih/4',           # Scale the images if needed to ensure dimensions are even
        # '-x264-params', 'subme=1',
        # '-x264-params', 'partitions=-parti4x4,-parti8x8,-partp8x8,-partp4x4,-partb8x8', 
        os.path.join(output_base_dir, video_name + ".mp4")  # Output video path
    ])

if __name__=="__main__":

    input_base_dir = "datasets/REDS/train_sharp"    # Update this with the path to your images
    output_base_dir = "REDS_H264_OUTPUT"            # Path for the output video

    os.system(f"rm {output_base_dir}/*")

    if not os.path.exists(output_base_dir):
        os.makedirs(output_base_dir)

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(merge_images_to_h264, input_base_dir, video_name, output_base_dir) for video_name in os.listdir(input_base_dir)]
        for future in as_completed(futures):
            future.result()  # If there's any exception, it will be raised here

        
