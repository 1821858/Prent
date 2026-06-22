import os
import sys
from types import SimpleNamespace

import cv2
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import Effects


IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif"}
VIDEO_EXTS = {".mp4", ".mov", ".avi", ".mkv", ".webm"}


def create_preview_page(parent, state, show_home_callback):
    return PreviewPage(parent, state, show_home_callback)


class PreviewPage(ttk.Frame):
    def __init__(self, parent, state, show_home_callback):
        super().__init__(parent)
        self.state = state
        self.show_home_callback = show_home_callback

        self.original_frame = None
        self.filtered_frame = None

        self.original_photo = None
        self.filtered_photo = None

        self.effect_var = tk.StringVar(value=getattr(state, "effect_name", "polygonize"))
        self.num_colors_var = tk.IntVar(value=getattr(state, "num_colors", 8))
        self.num_polygons_var = tk.IntVar(value=getattr(state, "num_polygons", 100))
        self.status_var = tk.StringVar(value="Ready")

        self._build_ui()

        self.after(100, self._load_source_preview)

    def _build_ui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        top = ttk.Frame(self)
        top.grid(row=0, column=0, sticky="ew", padx=16, pady=12)
        top.columnconfigure(1, weight=1)

        ttk.Button(top, text="Back", command=self.show_home_callback).grid(row=0, column=0, sticky="w")
        ttk.Label(top, text="Preview", font=("Helvetica", 24, "bold")).grid(
            row=0, column=1, sticky="w", padx=20
        )

        content = ttk.Frame(self)
        content.grid(row=1, column=0, sticky="nsew", padx=16, pady=16)
        content.columnconfigure(0, weight=1)
        content.rowconfigure(0, weight=1)
        content.rowconfigure(1, weight=0)

        compare_frame = ttk.Frame(content)
        compare_frame.grid(row=0, column=0, sticky="nsew")
        compare_frame.columnconfigure(0, weight=1)
        compare_frame.columnconfigure(1, weight=1)
        compare_frame.rowconfigure(2, weight=1)

        self.file_label = ttk.Label(compare_frame, text="", font=("Helvetica", 12))
        self.file_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 8))

        ttk.Label(compare_frame, text="Original", font=("Helvetica", 14, "bold")).grid(
            row=1, column=0, sticky="w", pady=(0, 6)
        )
        ttk.Label(compare_frame, text="Filtered", font=("Helvetica", 14, "bold")).grid(
            row=1, column=1, sticky="w", pady=(0, 6)
        )

        self.original_canvas = tk.Canvas(compare_frame, bg="#111111", highlightthickness=0, height=450)
        self.original_canvas.grid(row=2, column=0, sticky="nsew", padx=(0, 8))

        self.filtered_canvas = tk.Canvas(compare_frame, bg="#111111", highlightthickness=0, height=450)
        self.filtered_canvas.grid(row=2, column=1, sticky="nsew", padx=(8, 0))

        self.original_canvas.bind("<Configure>", self._canvas_resized)
        self.filtered_canvas.bind("<Configure>", self._canvas_resized)

        controls = ttk.LabelFrame(content, text="Effects Controls")
        controls.grid(row=1, column=0, sticky="ew", pady=(16, 0))
        controls.columnconfigure(1, weight=1)

        ttk.Label(controls, text="Effect").grid(row=0, column=0, sticky="w", padx=12, pady=(12, 4))
        self.effect_box = ttk.Combobox(
            controls,
            textvariable=self.effect_var,
            values=Effects.get_available_effects(),
            state="readonly",
            width=24,
        )
        self.effect_box.grid(row=0, column=1, sticky="w", padx=12, pady=(12, 4))
        self.effect_box.bind("<<ComboboxSelected>>", lambda event: self.update_preview())

        ttk.Label(controls, text="Num Colors").grid(row=1, column=0, sticky="w", padx=12, pady=4)
        self.colors_spin = ttk.Spinbox(controls, from_=1, to=64, textvariable=self.num_colors_var, width=10)
        self.colors_spin.grid(row=1, column=1, sticky="w", padx=12, pady=4)

        ttk.Label(controls, text="Num Polygons").grid(row=2, column=0, sticky="w", padx=12, pady=4)
        self.polygons_spin = ttk.Spinbox(controls, from_=1, to=1000, textvariable=self.num_polygons_var, width=10)
        self.polygons_spin.grid(row=2, column=1, sticky="w", padx=12, pady=4)

        button_row = ttk.Frame(controls)
        button_row.grid(row=3, column=0, columnspan=2, sticky="ew", padx=12, pady=(12, 8))
        button_row.columnconfigure(0, weight=1)
        button_row.columnconfigure(1, weight=1)

        ttk.Button(button_row, text="Update Preview", command=self.update_preview).grid(
            row=0, column=0, sticky="ew", padx=(0, 8)
        )
        ttk.Button(button_row, text="Export Output", command=self.export_output).grid(
            row=0, column=1, sticky="ew", padx=(8, 0)
        )

        ttk.Label(controls, textvariable=self.status_var).grid(
            row=4, column=0, columnspan=2, sticky="w", padx=12, pady=(0, 12)
        )

    def _canvas_resized(self, event):
        if self.original_frame is not None:
            self._display_frame(self.original_canvas, self.original_frame, which="original")

        if self.filtered_frame is not None:
            self._display_frame(self.filtered_canvas, self.filtered_frame, which="filtered")

    def _get_ext(self):
        path = getattr(self.state, "file_path", None)
        if not path:
            return ""
        return os.path.splitext(path)[1].lower()

    def _load_source_preview(self):
        path = getattr(self.state, "file_path", None)
        if not path:
            self.status_var.set("No file selected")
            return

        ext = self._get_ext()
        self.file_label.config(text=f"Selected: {os.path.basename(path)}")

        if ext in IMAGE_EXTS:
            image = cv2.imread(path)
            if image is None:
                self.status_var.set("Could not read image")
                return
            self.original_frame = image

        elif ext in VIDEO_EXTS:
            cap = cv2.VideoCapture(path)
            ok, frame = cap.read()
            cap.release()
            if not ok:
                self.status_var.set("Could not read video")
                return
            self.original_frame = frame

        else:
            self.status_var.set("Unsupported file type")
            return

        self.update_preview()

    def _effect_args(self):
        return SimpleNamespace(
            num_colors=int(self.num_colors_var.get()),
            num_polygons=int(self.num_polygons_var.get()),
        )

    def _display_frame(self, canvas, frame, which="filtered"):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb)

        canvas.update_idletasks()
        canvas_w = max(canvas.winfo_width() - 20, 100)
        canvas_h = max(canvas.winfo_height() - 20, 100)

        img.thumbnail((canvas_w, canvas_h))

        photo = ImageTk.PhotoImage(img)

        if which == "original":
            self.original_photo = photo
        else:
            self.filtered_photo = photo

        canvas.delete("all")
        canvas_w = max(canvas.winfo_width(), 1)
        canvas_h = max(canvas.winfo_height(), 1)
        canvas.create_image(canvas_w // 2, canvas_h // 2, image=photo)

    def update_preview(self):
        if self.original_frame is None:
            self.status_var.set("No preview available")
            return

        effect_name = self.effect_var.get()
        effect_fn = Effects.get_effect_function(effect_name)

        if effect_fn is None:
            self.status_var.set("Unknown effect")
            return

        try:
            self.state.effect_name = effect_name
            self.state.num_colors = int(self.num_colors_var.get())
            self.state.num_polygons = int(self.num_polygons_var.get())

            args = self._effect_args()
            self.filtered_frame = effect_fn(self.original_frame.copy(), args)

            self._display_frame(self.original_canvas, self.original_frame, which="original")
            self._display_frame(self.filtered_canvas, self.filtered_frame, which="filtered")

            self.status_var.set("Preview updated")
        except Exception as e:
            self.status_var.set(f"Preview error: {e}")

    def export_output(self):
        path = getattr(self.state, "file_path", None)
        if not path:
            messagebox.showerror("Error", "No input file selected.")
            return

        effect_name = self.effect_var.get()
        effect_fn = Effects.get_effect_function(effect_name)
        if effect_fn is None:
            messagebox.showerror("Error", "Please choose a valid effect.")
            return

        ext = self._get_ext()
        directory = os.path.dirname(path)
        name = os.path.splitext(os.path.basename(path))[0]
        args = self._effect_args()

        try:
            self.status_var.set("Exporting...")
            self.update_idletasks()

            if ext in IMAGE_EXTS:
                image = cv2.imread(path)
                if image is None:
                    raise RuntimeError("Could not read image.")

                processed = effect_fn(image, args)
                output_path = os.path.join(directory, f"{name}_{effect_name}{ext}")
                ok = cv2.imwrite(output_path, processed)
                if not ok:
                    raise RuntimeError("Failed to save image.")

            elif ext in VIDEO_EXTS:
                cap = cv2.VideoCapture(path)
                if not cap.isOpened():
                    raise RuntimeError("Could not open video.")

                fps = cap.get(cv2.CAP_PROP_FPS)
                if not fps or fps <= 0:
                    fps = 30

                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

                output_path = os.path.join(directory, f"{name}_{effect_name}.mp4")
                fourcc = cv2.VideoWriter_fourcc(*"mp4v")
                out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

                frame_count = 0
                while True:
                    ok, frame = cap.read()
                    if not ok:
                        break

                    processed = effect_fn(frame, args)
                    out.write(processed)

                    frame_count += 1
                    self.status_var.set(f"Exporting... frame {frame_count}")
                    self.update_idletasks()

                cap.release()
                out.release()

            else:
                raise RuntimeError("Unsupported file type.")

            self.status_var.set(f"Saved: {output_path}")
            messagebox.showinfo("Done", f"Saved output to:\n{output_path}")

        except Exception as e:
            self.status_var.set(f"Export error: {e}")
            messagebox.showerror("Export failed", str(e))