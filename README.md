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
ffmpeg (for HLS stream download)

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

When you install FFmpeg, the installer should automatically add the FFmpeg bin folder to your system's PATH variable. However, if it doesn't, or if you installed FFmpeg manually, you may need to add the FFmpeg bin folder to your PATH manually.
Here's how you can check if FFmpeg is in your system's PATH and add it if it's not:

Open a terminal or command prompt.
Type ffmpeg and press Enter. If you get a message saying "ffmpeg is not recognized as an internal or external command", it means FFmpeg is not in your PATH.
To add FFmpeg to your PATH, you need to find the folder where you installed FFmpeg (e.g., C:\FFmpeg\bin on Windows or /usr/local/bin on macOS/Linux).
On Windows:

Open the Start menu and search for "Environment Variables".
Click "Edit the system environment variables".
Click the "Environment Variables" button.
Under "System Variables", scroll down and find the "Path" variable, then click "Edit".
Click "New" and paste the path to the FFmpeg bin folder (e.g., C:\FFmpeg\bin).
Click "OK" to save the changes.


On macOS/Linux:

Open a terminal.
Edit your shell configuration file (e.g., .bashrc, .zshrc, etc.) using a text editor.
Add the following line at the end of the file: export PATH="/path/to/ffmpeg/bin:$PATH" (replace /path/to/ffmpeg/bin with the actual path to your FFmpeg bin folder).
Save the file and restart your terminal or run source /path/to/your/shell/config/file to apply the changes.



After adding FFmpeg to your PATH, you should be able to run the ffmpeg command from any directory, and the Python script should be able to find and execute the ffmpeg binary without any issues.


Contributing
Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.
