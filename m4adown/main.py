#!/usr/bin/env python3
import subprocess
import tkinter as tk
from tkinter import messagebox, filedialog
import os

download_dir = os.path.expanduser("~/Music")

def choose_directory():
    global download_dir
    folder = filedialog.askdirectory()
    if folder:
        download_dir = folder
        folder_label.config(text=f"Selected folder: {download_dir}")

def download_audio():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube link.")
        return

    outtmpl = os.path.join(download_dir, "%(title)s.%(ext)s")

    command = [
        "yt-dlp",
        "-f", "m4a",
        "--extract-audio",
        "--audio-format", "m4a",
        "--audio-quality", "192K",
        "--embed-metadata",
        "--embed-thumbnail",
        "--add-metadata",
        "-o", outtmpl,
        url
    ]

    try:
        subprocess.run(command, check=True)
        messagebox.showinfo("Successful", f"Download completed!\n{download_dir}")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "There was a problem during the download.")

# ---------------- GUI ----------------
root = tk.Tk()
root.title("m4adown - YouTube M4A downloader")
root.geometry("500x200")

tk.Label(root, text="YouTube Link:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

folder_button = tk.Button(root, text="Select folder", command=choose_directory)
folder_button.pack(pady=5)

folder_label = tk.Label(root, text=f"Selected folder: {download_dir}")
folder_label.pack(pady=5)

download_button = tk.Button(root, text="Download", command=download_audio)
download_button.pack(pady=10)

root.mainloop()
