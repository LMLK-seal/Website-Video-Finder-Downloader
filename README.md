Website Video Finder & Downloader

Website Video Finder & Downloader is a Python application that helps you find and download video streams from websites. It can detect and download direct video files, HLS (m3u8) streams, and MPEG-DASH streams (MPEG-DASH download is not yet supported).
Features

Find video streams on websites, including those loaded by JavaScript
Download direct video files (e.g., MP4, WebM)
Download HLS (m3u8) streams using ffmpeg
Preview video thumbnails (not implemented yet)
User-friendly GUI interface

Prerequisites
Before running the application, ensure you have the following dependencies installed:

Python 3.x
Google Chrome (for Selenium)
ffmpeg (for HLS stream download - you can download the code directly to FFmpeg bin folder.)

You can install the required Python packages using pip:
Copy codepip install -r requirements.txt

Usage

1. Run the WebsiteVideoFinder&Downloader.py script.
2. Enter the full website URL in the entry field (e.g., https://www.example.com).
3. Click the "Find Videos" button to search for video streams on the webpage.
4. Select a video from the list.
5. Click the "Download Selected Video" button to download the video file.

Note: 
For HLS (m3u8) streams, the application will download and combine the individual segments using ffmpeg.
Contributing
Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.
