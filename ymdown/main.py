#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import subprocess
import os

download_dir = os.path.expanduser("~/Music")

class Downloader(Gtk.Window):
    def __init__(self):
        super().__init__(title="You Music Downloader")
        self.set_default_size(500, 200)

        self.url_entry = Gtk.Entry()
        self.url_entry.set_placeholder_text("YouTube link...")

        # Layout
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_margin_top(10)
        vbox.set_margin_bottom(10)
        vbox.set_margin_start(10)
        vbox.set_margin_end(10)
        self.add(vbox)

        # URL label sola yaslı
        label_url = Gtk.Label(label="YouTube Link:")
        label_url.set_xalign(0)
        vbox.pack_start(label_url, False, False, 0)
        vbox.pack_start(self.url_entry, False, False, 0)

        folder_button = Gtk.Button(label="Select folder")
        folder_button.connect("clicked", self.choose_directory)
        vbox.pack_start(folder_button, False, False, 0)

        # Folder label sola yaslı
        self.folder_label = Gtk.Label(label=f"Selected folder: {download_dir}")
        self.folder_label.set_xalign(0)
        vbox.pack_start(self.folder_label, False, False, 0)

        # Buttons
        hbox = Gtk.Box(spacing=10)
        hbox.pack_start(Gtk.Label(label="Download as:"), False, False, 0)

        m4a_button = Gtk.Button(label="M4A")
        m4a_button.connect("clicked", lambda w: self.download_audio("m4a"))
        hbox.pack_start(m4a_button, False, False, 0)

        mp3_button = Gtk.Button(label="MP3")
        mp3_button.connect("clicked", lambda w: self.download_audio("mp3"))
        hbox.pack_start(mp3_button, False, False, 0)

        vbox.pack_start(hbox, False, False, 0)

    def choose_directory(self, widget):
        dialog = Gtk.FileChooserDialog(
            title="Select folder",
            parent=self,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        if dialog.run() == Gtk.ResponseType.OK:
            global download_dir
            download_dir = dialog.get_filename()
            self.folder_label.set_text(f"Selected folder: {download_dir}")

        dialog.destroy()

    def download_audio(self, format_type):
        url = self.url_entry.get_text().strip()
        if not url:
            self.show_message("Error", "Please enter a YouTube link.")
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
            url,
            "--extractor-args" "'youtube:player-client=default,-tv_simply'"
        ]

        try:
            subprocess.run(command, check=True)
            self.show_message("Successful", f"Download completed!\n{download_dir}")
        except subprocess.CalledProcessError:
            self.show_message("Error", "There was a problem during the download.")

    def show_message(self, title, message):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.INFO if title == "Successful" else Gtk.MessageType.ERROR,
            buttons=Gtk.ButtonsType.OK,
            text=title,
        )
        dialog.format_secondary_text(message)
        dialog.run()
        dialog.destroy()


def main():
    win = Downloader()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
