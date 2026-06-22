from dataclasses import dataclass
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from Home import create_home_page
from Preview import create_preview_page
from Help import create_help_page
from About import create_about_page


IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif"}
VIDEO_EXTS = {".mp4", ".mov", ".avi", ".mkv", ".webm"}


@dataclass
class AppState:
    file_path: str | None = None
    effect_name: str = "polygonize"
    num_polygons: int = 100
    num_colors: int = 8


class PrentApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Prent")

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        dynamic_width = int(screen_width * 0.75)
        dynamic_height = int(screen_height * 0.75)
        x = int((screen_width - dynamic_width) / 2)
        y = int((screen_height - dynamic_height) / 2)
        self.root.geometry(f"{dynamic_width}x{dynamic_height}+{x}+{y}")

        self.state = AppState()

        self.container = ttk.Frame(self.root)
        self.container.pack(fill=tk.BOTH, expand=True)

        self.current_frame = None
        self.show_home()

    def _clear(self):
        if self.current_frame is not None:
            self.current_frame.destroy()
            self.current_frame = None

    def browse_file(self):
        path = filedialog.askopenfilename(
            title="Choose an image or video",
            filetypes=[
                ("Media files", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif *.mp4 *.mov *.avi *.mkv *.webm"),
                ("Images", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif"),
                ("Videos", "*.mp4 *.mov *.avi *.mkv *.webm"),
                ("All files", "*.*"),
            ],
        )
        if not path:
            return

        ext = os.path.splitext(path)[1].lower()
        if ext not in IMAGE_EXTS and ext not in VIDEO_EXTS:
            messagebox.showerror(
                "Invalid file",
                "Please choose a valid image or video file.",
            )
            return

        self.state.file_path = path
        self.show_preview()

    def show_home(self):
        self._clear()
        self.current_frame = create_home_page(
            self.container,
            browse_callback=self.browse_file,
            show_help_callback=self.show_help,
            show_about_callback=self.show_about,
            state=self.state,
        )
        self.current_frame.pack(fill=tk.BOTH, expand=True)

    def show_preview(self):
        if not self.state.file_path:
            self.show_home()
            return

        self._clear()
        self.current_frame = create_preview_page(
            self.container,
            state=self.state,
            show_home_callback=self.show_home,
        )
        self.current_frame.pack(fill=tk.BOTH, expand=True)

    def show_help(self):
        self._clear()
        self.current_frame = create_help_page(self.container, self.show_home)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

    def show_about(self):
        self._clear()
        self.current_frame = create_about_page(self.container, self.show_home)
        self.current_frame.pack(fill=tk.BOTH, expand=True)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    PrentApp().run()