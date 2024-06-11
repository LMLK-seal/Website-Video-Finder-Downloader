import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse
import ssl
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import re
import json
import m3u8
import subprocess

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-web-security")  # This can help bypass CORS issues
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def extract_json_objects(text, decoder=json.JSONDecoder()):
    pos = 0
    while True:
        match = text.find('{', pos)
        if match == -1:
            break
        try:
            result, index = decoder.raw_decode(text[match:])
            yield (result, match, match + index)
            pos = match + index
        except:
            pos = match + 1

def find_video_urls(driver, base_url):
    video_urls = []

    # Regular video tags
    for video in driver.find_elements(By.TAG_NAME, "video"):
        src = video.get_attribute("src")
        if src:
            video_urls.append((src, "video", None))

    # Look for video URLs in page source
    page_source = driver.page_source
    
    # HLS (m3u8) patterns
    m3u8_pattern = r'https?://[^\s"\']+\.m3u8[^\s"\']*'
    for match in re.finditer(m3u8_pattern, page_source):
        video_urls.append((match.group(0), "hls", None))
    
    # MPEG-DASH patterns
    mpd_pattern = r'https?://[^\s"\']+\.mpd[^\s"\']*'
    for match in re.finditer(mpd_pattern, page_source):
        video_urls.append((match.group(0), "dash", None))
    
    # Look in JavaScript objects for video URLs
    for obj, _, _ in extract_json_objects(page_source):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if 'video' in key.lower() and isinstance(value, str) and any(ext in value for ext in ['.mp4', '.webm', '.m3u8', '.mpd']):
                    type_ = 'hls' if '.m3u8' in value else 'dash' if '.mpd' in value else 'direct'
                    video_urls.append((urljoin(base_url, value), type_, None))

    return video_urls

def download_hls_video(url, save_path):
    m3u8_obj = m3u8.load(url)
    base_uri = m3u8_obj.base_uri or os.path.dirname(url)
    
    with open("temp.m3u8", "w") as f:
        f.write(m3u8_obj.dumps())
    
    # Use ffmpeg to download and combine segments
    ffmpeg_cmd = [
        "ffmpeg", "-protocol_whitelist", "file,http,https,tcp,tls",
        "-allowed_extensions", "ALL", "-i", "temp.m3u8", "-c", "copy", save_path
    ]
    subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove("temp.m3u8")

def download_video(url, type_, save_path):
    if type_ == "hls":
        download_hls_video(url, save_path)
    elif type_ == "dash":
        messagebox.showwarning("Warning", "MPEG-DASH download not yet supported. Use a browser extension.")
    else:  # direct video
        video_data = requests.get(url, headers=headers, verify=False).content
        with open(save_path, 'wb') as f:
            f.write(video_data)

def on_video_select(event):
    pass  # No preview for streaming videos

def download_selected_video():
    selected_items = video_list.selection()
    if not selected_items:
        messagebox.showwarning("Warning", "Please select a video.")
        return

    selected_item = selected_items[0]
    video_url, video_type, _ = video_list.item(selected_item)['values']

    save_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")])
    if save_path:
        try:
            download_video(video_url, video_type, save_path)
            messagebox.showinfo("Success", f"Video saved to {save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to download the video: {str(e)}")

def open_or_download_video():
    selected_items = video_list.selection()
    if not selected_items:
        messagebox.showwarning("Warning", "Please select a video.")
        return

    selected_item = selected_items[0]
    video_url, video_type, _ = video_list.item(selected_item)['values']

    if video_type in ["hls", "dash"]:
        download_selected_video()
    else:  # direct video
        save_path = filedialog.asksaveasfilename(defaultextension=".mp4", filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")])
        if save_path:
            try:
                download_video(video_url, video_type, save_path)
                messagebox.showinfo("Success", f"Video saved to {save_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to download the video: {str(e)}")

def fetch_videos():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a website URL.")
        return

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url

    try:
        update_status("Connecting to the website...")
        driver = setup_driver()
        driver.get(url)

        # Wait for video content to load
        time.sleep(5)  # Basic wait
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "video"))
            )
        except:
            pass  # Continue even if no video tag is found

        videos = find_video_urls(driver, url)
        driver.quit()

        if videos:
            update_status(f"Found {len(videos)} video streams. Select one to download.")
            for item in video_list.get_children():
                video_list.delete(item)
            for i, (video_url, video_type, _) in enumerate(videos, 1):
                video_list.insert("", "end", text=str(i), values=(video_url, video_type, "N/A"))
            video_list.selection_set(video_list.get_children()[0])
        else:
            messagebox.showwarning("Warning", "No video streams found on the webpage.")
            update_status("No video streams found.")

    except Exception as e:
        messagebox.showerror("Error", str(e))
        update_status("An error occurred.")

# Create main window
root = tk.Tk()
root.title("Website Video Finder & Downloader")

window_width = 800
window_height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# URL entry and fetch button
url_frame = tk.Frame(root)
url_frame.pack(pady=10, padx=10, fill=tk.X)

url_label = tk.Label(url_frame, text="Enter Website URL:", font=("Arial", 12))
url_label.pack(side=tk.LEFT, padx=5)

url_entry = tk.Entry(url_frame, width=50, font=("Arial", 10))
url_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
url_entry.focus()

fetch_button = tk.Button(url_frame, text="Find Videos", command=fetch_videos, font=("Arial", 10), bg="#4CAF50", fg="white")
fetch_button.pack(side=tk.LEFT, padx=5)

# Video list and preview
content_frame = tk.Frame(root)
content_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

video_list_frame = tk.Frame(content_frame)
video_list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

video_list = ttk.Treeview(video_list_frame, columns=("URL", "Type", "Thumbnail"), show="headings")
video_list.heading("URL", text="URL")
video_list.heading("Type", text="Type")
video_list.heading("Thumbnail", text="Thumbnail")
video_list.column("URL", width=400)
video_list.column("Type", width=100)
video_list.column("Thumbnail", width=100)
video_list.pack(fill=tk.BOTH, expand=True)
video_list.bind("<<TreeviewSelect>>", on_video_select)

preview_frame = tk.Frame(content_frame)
preview_frame.pack(side=tk.RIGHT, padx=10)

preview_label = tk.Label(preview_frame, text="Video Thumbnail", compound=tk.TOP)
preview_label.pack()

# Open/Download button
action_button = tk.Button(root, text="Download Selected Video", command=open_or_download_video, font=("Arial", 12), bg="#008CBA", fg="white")
action_button.pack(pady=10)

# Status label
status_label = tk.Label(root, text="", font=("Arial", 10), fg="#333333")
status_label.pack(pady=5)

def update_status(message):
    status_label.config(text=message)
    root.update_idletasks()

# Help text
help_text = """
1. Enter the full website URL (e.g., https://www.example.com).
2. Click 'Find Videos' to search for videos on the page.
3. Select a video from the list.
4. Click 'Open/Download Selected Video' to download the file.

Note: This tool can find videos loaded by JavaScript!
It detects direct video files, HLS (m3u8), and MPEG-DASH streams.
MPEG-DASH download is not yet supported.

Created by: LMLK - Imperial Seal.
"""
help_label = tk.Label(root, text=help_text, justify=tk.LEFT, fg="#555555", font=("Arial", 8))
help_label.pack(pady=10, padx=20, anchor="w")

# Global headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Disable SSL verification (use with caution)
ssl._create_default_https_context = ssl._create_unverified_context

# Run the GUI
root.mainloop()
