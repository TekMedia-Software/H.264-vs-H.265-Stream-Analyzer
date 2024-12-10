# Installation Guide

This document provides step-by-step instructions for installing the **H.264 vs H.265 Video Comparison** Project.

## Prerequisites

Before you begin, ensure you have the following requirements:

- Python: Version 3 or higher
- FFmpeg >= 5.0 Required for video analysis build with **libvmaf**
- PyQt5: For the graphical user interface
- Matplotlib: For visualizing the graphical comparison

## Installation Steps									

1. Clone the repository:

        git clone tekmedia@192.168.0.225:~/git/TekMedia/H.264_vs_H.265_Stream-Analyzer

2. Navigate to the project directory:

        cd H.264_vs_H.265_Stream-Analyzer

3. Install dependencies:

- Install Python dependencies:

        pip install -r requirements.txt

- Install FFmpeg:

    Ensure FFmpeg >= 5.0 is installed with libvmaf enabled and accessible in your system’s PATH.
    
    To check installation:

        ffmpeg -version
    Ensure libvmaf is enabled.
    
## Running the Project

To start the project after installation, use the following command:

        python3 app.py

## Contact

For any questions or feedback, please reach out:

- *Awadh Bajpai* - [awabaj@tekmediasoft.net](mailto:awabaj@tekmediasoft.net)
- *Sushanthika Manikandan* - [susman@tekmediasoft.net](mailto:susman@tekmediasoft.net)
