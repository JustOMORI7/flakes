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

def download_audio(format_type):
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "Please enter a YouTube link.")
        return

    outtmpl = os.path.join(download_dir, "%(title)s.%(ext)s")

    command = [
        "yt-dlp",
        "--extract-audio",
        "--audio-format", format_type,
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
root.title("You Music Downloader")
root.geometry("500x220")

tk.Label(root, text="YouTube Link:").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

folder_button = tk.Button(root, text="Select folder", command=choose_directory)
folder_button.pack(pady=5)

folder_label = tk.Label(root, text=f"Selected folder: {download_dir}")
folder_label.pack(pady=5)

buttons_frame = tk.Frame(root)
buttons_frame.pack(pady=5)

tk.Label(buttons_frame, text="Download as:").pack(side="left", padx=5)

m4a_button = tk.Button(buttons_frame, text="M4A", width=10, command=lambda: download_audio("m4a"))
m4a_button.pack(side="left", padx=5)

mp3_button = tk.Button(buttons_frame, text="MP3", width=10, command=lambda: download_audio("mp3"))
mp3_button.pack(side="left", padx=5)

root.mainloop()
