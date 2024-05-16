# h264_decode (GPT Gen)

## Overview
The `h264_decode` repository is designed to explore and test the decoding of H.264 bitstreams using Python, specifically focusing on intra-frame prediction techniques. This project originates from experiments with the JM (Joint Model) reference software version 16.1, tailored for decoding H.264 bitstreams.

## Current Functionality
As of now, the repository contains preliminary Python scripts that facilitate the decoding process with an emphasis on intra-frame prediction. The current implementation is experimental and aims to decode the bitstreams to raw traces, primarily focusing on intra-prediction modes.

## Problem Statement
The intra-frame prediction currently does not perform adequately:
- The prediction mode for blocks of size 8x8 and 4x4 is not present after decoding to traces.
- The Inverse Discrete Cosine Transform (IDCT) results are suboptimal for block sizes 8x8 and 4x4 when compared to a 16x16 block. Notably, IDCT is only effectively applied in a 4x4 area, regardless of the original block size.

## Repository Structure
- `REDS_264_bitstream_OUTPUT/` - Output directory for bitstream operations.
- `REDS_264_trace_OUTPUT/` - Output directory for trace operations.
- `H264_OUTPUT/` - General output directory for H.264 decoding.
- `jm_16.1/` - Contains JM reference software version 16.1 used for generating test bitstreams.
- `scripts/` - Contains Python scripts for the conversion and processing tasks:
  - `p1_pngs2h264.py` - Converts PNG images to H.264 bitstream.
  - `p2_h264_to_bitstream.py` - Extracts bitstream from H.264 video.
  - `p3_bitstream_to_traces.py` - Converts bitstream to trace files for analysis.
  - `png2h264_intra_only_parallel.py` - Handles intra-frame prediction in parallel.
- `i_frame_decoder.py` - Script focused on intra-frame decoding.
- `reds_264_decode.ipynb` - Jupyter notebook detailing the decoding process and issues.

## Getting Started
To get started with this project:
1. Clone the repository.
2. Ensure Python 3.x is installed on your machine.
3. Install required dependencies: `pip install -r requirements.txt` (to be added).
4. Explore the `reds_264_decode.ipynb` for a step-by-step guide on the current decoding process and intra-frame prediction challenges.

## How to Contribute
Contributions are welcome, especially from those with expertise in video compression and Python programming. To contribute:
1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Develop your feature or fix.
4. Submit a pull request against the main branch.

## Seeking Help
We are specifically seeking help in improving the intra-frame prediction algorithms and enhancing the IDCT results for various block sizes. Any insights, code enhancements, or suggestions in these areas would be greatly appreciated.
