# This is step 3 to convert h264 bitstream files (*.264) to Traces (*.xml) and Raw Outputs (*.yuv). 
# IN PATH@REDS_264_CONTAINER_OUTPUT/
# 000.264
# 001.264
# ...
# 169.264

import subprocess
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Directory containing the images

def save_bitstream_to_trace_and_raw(input_base_dir, video_name, output_base_dir):

    subprocess.run([
        './jm_16.1/bin/ldecod.exe',
        '-i', os.path.join(input_base_dir, 
                           video_name + ".264"),  # Input .264 file
        '-o', os.path.join(output_base_dir, 
                           video_name + ".yuv"),  # Output .yuv file
        '-xmltrace', os.path.join(output_base_dir, 
                                  video_name + ".xml")  # XML trace file
    ])


if __name__=="__main__":

    input_base_dir = "REDS_264_bitstream_OUTPUT"    # Update this with the path to your images
    output_base_dir = "REDS_264_trace_OUTPUT"            # Path for the output video

    os.system(f"rm {output_base_dir}/*")

    if not os.path.exists(output_base_dir):
        os.makedirs(output_base_dir)

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(save_bitstream_to_trace_and_raw, 
                                   input_base_dir, video_name[:-4], output_base_dir) 
                    for video_name in os.listdir(input_base_dir)]
        for future in as_completed(futures):
            future.result()  # If there's any exception, it will be raised here

        
