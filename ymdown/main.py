#!/usr/bin/env python3
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
import subprocess
import os

download_dir = os.path.expanduser("~/Music")

class Downloader(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title="You Music Downloader")
        self.set_default_size(500, 200)

        self.url_entry = Gtk.Entry()
        self.url_entry.set_placeholder_text("YouTube link...")

        # Layout
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_margin_top(10)
        vbox.set_margin_bottom(10)
        vbox.set_margin_start(10)
        vbox.set_margin_end(10)
        self.set_child(vbox)

        # URL label sola yaslı
        label_url = Gtk.Label(label="YouTube Link:")
        label_url.set_xalign(0)
        vbox.append(label_url)
        vbox.append(self.url_entry)

        folder_button = Gtk.Button(label="Select folder")
        folder_button.connect("clicked", self.choose_directory)
        vbox.append(folder_button)

        # Folder label sola yaslı
        self.folder_label = Gtk.Label(label=f"Selected folder: {download_dir}")
        self.folder_label.set_xalign(0)
        vbox.append(self.folder_label)

        # Buttons
        hbox = Gtk.Box(spacing=10)
        label_dl = Gtk.Label(label="Download as:")
        label_dl.set_xalign(0)
        hbox.append(label_dl)

        m4a_button = Gtk.Button(label="M4A")
        m4a_button.connect("clicked", lambda w: self.download_audio("m4a"))
        hbox.append(m4a_button)

        mp3_button = Gtk.Button(label="MP3")
        mp3_button.connect("clicked", lambda w: self.download_audio("mp3"))
        hbox.append(mp3_button)

        vbox.append(hbox)

    def choose_directory(self, widget):
        dialog = Gtk.FileChooserNative(
            title="Select folder",
            transient_for=self,
            action=Gtk.FileChooserAction.SELECT_FOLDER,
            accept_label="Select",
            cancel_label="Cancel"
        )

        def on_response(dlg, response):
            if response == Gtk.ResponseType.ACCEPT:
                global download_dir
                file = dlg.get_file()
                if file:
                    download_dir = file.get_path()
                    self.folder_label.set_text(f"Selected folder: {download_dir}")
            dlg.destroy()

        dialog.connect("response", on_response)
        dialog.show()


    def download_audio(self, format_type):
        url = self.url_entry.get_text().strip()
        if not url:
            self.show_message("Error", "Please enter a YouTube link.", Gtk.MessageType.ERROR)
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
            self.show_message("Successful", f"Download completed!\n{download_dir}", Gtk.MessageType.INFO)
        except subprocess.CalledProcessError:
            self.show_message("Error", "There was a problem during the download.", Gtk.MessageType.ERROR)

    def show_message(self, title, message, msg_type):
        dialog = Gtk.MessageDialog(
            transient_for=self,
            modal=True,
            message_type=msg_type,
            buttons=Gtk.ButtonsType.OK,
            text=title,
        )

        if message:
            dialog.set_markup(f"<b>{title}</b>\n\n{message}")

        dialog.connect("response", lambda d, r: d.destroy())
        dialog.show()



class DownloaderApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.example.YouMusicDownloader")

    def do_activate(self):
        win = Downloader(self)
        win.present()


def main():
    app = DownloaderApp()
    app.run()


if __name__ == "__main__":
    main()
