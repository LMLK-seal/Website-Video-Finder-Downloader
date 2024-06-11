<h1 style="font-family:Arial; color:#333333;">Website Video Finder & Downloader</h1>

<p style="font-family:Georgia; font-size:16px;">Website Video Finder & Downloader is a Python application that helps you find and download video streams from websites. It can detect and download direct video files, HLS (m3u8) streams, and MPEG-DASH streams (MPEG-DASH download is not yet supported).</p>

<h2 style="font-family:Verdana; color:#007acc;">Features</h2>

<ul style="font-family:Tahoma; font-size:14px;">
  <li>Find video streams on websites, including those loaded by JavaScript</li>
  <li>Download direct video files (e.g., MP4, WebM)</li>
  <li>Download HLS (m3u8) streams using ffmpeg</li>
  <li>Preview video thumbnails (not implemented yet)</li>
  <li>User-friendly GUI interface</li>
</ul>

<h2 style="font-family:Verdana; color:#007acc;">Prerequisites</h2>

<p style="font-family:Georgia; font-size:16px;">Before running the application, ensure you have the following dependencies installed:</p>

<ul style="font-family:Tahoma; font-size:14px;">
  <li>Python 3.x</li>
  <li>Google Chrome (for Selenium)</li>
  <li>ffmpeg (for HLS stream download)</li>
</ul>

<p style="font-family:Georgia; font-size:16px;">You can install the required Python packages using pip:</p>

```
pip install -r requirements.txt
```

<p style="font-family:Georgia; font-size:16px;">or you can install them separately:</p>

```
pip install tkinter
pip install requests
pip install beautifulsoup4
pip install selenium
pip install webdriver-manager
pip install m3u8
```

<h2 style="font-family:Verdana; color:#007acc;">Usage</h2>

<ol style="font-family:Tahoma; font-size:14px;">
  <li>Run the <code>WebsiteVideoFinder&Downloader.py</code> script.</li>
  <li>Enter the full website URL in the entry field (e.g., <code>https://www.example.com</code>).</li>
  <li>Click the "Find Videos" button to search for video streams on the webpage.</li>
  <li>Select a video from the list.</li>
  <li>Click the "Download Selected Video" button to download the video file.</li>
</ol>

<p style="font-family:Georgia; font-size:16px;"><strong>Note:</strong> For HLS (m3u8) streams, the application will download and combine the individual segments using ffmpeg.</p>

<h3 style="font-family:Verdana; color:#007acc;">FFmpeg Installation</h3>

<p style="font-family:Georgia; font-size:16px;">When you install FFmpeg, the installer should automatically add the FFmpeg bin folder to your system's <code>PATH</code> variable. However, if it doesn't, or if you installed FFmpeg manually, you may need to add the FFmpeg bin folder to your <code>PATH</code> manually. Here's how you can check if FFmpeg is in your system's <code>PATH</code> and add it if it's not:</p>

<ol style="font-family:Tahoma; font-size:14px;">
  <li>Open a terminal or command prompt.</li>
  <li>Type <code>ffmpeg</code> and press Enter. If you get a message saying "<code>ffmpeg</code> is not recognized as an internal or external command", it means FFmpeg is not in your <code>PATH</code>.</li>
  <li>To add FFmpeg to your <code>PATH</code>, you need to find the folder where you installed FFmpeg (e.g., <code>C:\FFmpeg\bin</code> on Windows or <code>/usr/local/bin</code> on macOS/Linux).</li>
</ol>

<p style="font-family:Georgia; font-size:16px;"><strong>On Windows:</strong></p>

<ul style="font-family:Tahoma; font-size:14px;">
  <li>Open the Start menu and search for "Environment Variables".</li>
  <li>Click "Edit the system environment variables".</li>
  <li>Click the "Environment Variables" button.</li>
  <li>Under "System Variables", scroll down and find the "Path" variable, then click "Edit".</li>
  <li>Click "New" and paste the path to the FFmpeg bin folder (e.g., <code>C:\FFmpeg\bin</code>).</li>
  <li>Click "OK" to save the changes.</li>
</ul>

<p style="font-family:Georgia; font-size:16px;"><strong>On macOS/Linux:</strong></p>

<ul style="font-family:Tahoma; font-size:14px;">
  <li>Open a terminal.</li>
  <li>Edit your shell configuration file (e.g., <code>.bashrc</code>, <code>.zshrc</code>, etc.) using a text editor.</li>
  <li>Add the following line at the end of the file: <code>export PATH="/path/to/ffmpeg/bin:$PATH"</code> (replace <code>/path/to/ffmpeg/bin</code> with the actual path to your FFmpeg bin folder).</li>
  <li>Save the file and restart your terminal or run <code>source /path/to/your/shell/config/file</code> to apply the changes.</li>
</ul>

<p style="font-family:Georgia; font-size:16px;">After adding FFmpeg to your <code>PATH</code>, you should be able to run the <code>ffmpeg</code> command from any directory, and the Python script should be able to find and execute the <code>ffmpeg</code> binary without any issues.</p>

<h2 style="font-family:Verdana; color:#007acc;">Contributing</h2>

<p style="font-family:Georgia; font-size:16px;">Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.</p>
