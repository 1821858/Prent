from tkinter import *
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import os

def create_home_page(parent, show_help_callback, show_about_callback, selected_file=None):
    frame = Frame(parent)

    header_font = ("Helvetica", 50, "bold")
    subheader_font = ("Helvetica", 30)
    warning_font = ("Helvetica", 15, "italic")

    style = ttk.Style()
    style.configure("Home.TButton", font=subheader_font)

    ttk.Label(frame, text="Welcome to Prent!", font=header_font).pack(pady=[35, 0])
    ttk.Label(frame, text="To get started, please upload an image or video file.", font=subheader_font).pack(pady=10)

    error_one = ttk.Label(frame, text="Error: Your file is not a valid image or video file.",
                          font=warning_font, foreground='red')
    error_two = ttk.Label(frame, text="Acceptable file extensions are .jpg, .jpeg, .png, .bmp, .tiff, .tif, and .mp4.",
                          font=warning_font, foreground='red')

    selected_label = ttk.Label(frame, text="", font=("Helvetica", 18))
    selected_label.pack(pady=10)

    def hide_errors():
        error_one.pack_forget()
        error_two.pack_forget()

    def show_errors():
        error_one.pack(pady=10)
        error_two.pack(pady=10)

    def show_preview_screen(file_path):
        for widget in frame.winfo_children():
            widget.destroy()

        ext = os.path.splitext(file_path)[1].lower()
        filename = os.path.basename(file_path)

        ttk.Label(frame, text=f"Selected: {filename}", font=("Helvetica", 25, "bold")).pack(pady=20)

        if ext != ".mp4":
            try:
                # Image Preview
                img = Image.open(file_path)
                img.thumbnail((600, 400))
                tk_img = ImageTk.PhotoImage(img)

                preview_label = Label(frame, image=tk_img)
                preview_label.image = tk_img
                preview_label.pack(pady=20)
            except:
                ttk.Label(frame, text="Error displaying image preview", font=("Helvetica", 15, "italic"), foreground="red").pack(pady=20)
        else:
            # Video Preview
            ttk.Label(frame, text="Error displaying video preview", font=("Helvetica", 15, "italic"), foreground="red").pack(pady=20)

        ttk.Button(frame, text="Back", style="Home.TButton", command=lambda: go_home()).pack(pady=30, ipadx=10, ipady=10)

    def go_home():
        frame.destroy()
        new_page = create_home_page(parent, show_help_callback, show_about_callback, selected_file)
        new_page.pack(fill="both", expand=True)

    def browse_files():
        file_path = filedialog.askopenfilename(
            title="Select an Image or Video",
            filetypes=[
                ("Image/Video Files", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif *.mp4"),
                ("All Files", "*.*")
            ]
        )

        if not file_path:
            return

        ext = os.path.splitext(file_path)[1].lower()
        if ext in {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif", ".mp4"}:
            hide_errors()
            selected_label.config(text=f"Selected: {os.path.basename(file_path)}")

            #SEND TO MAIN
            if selected_file:
                selected_file(file_path)

            show_preview_screen(file_path)
        else:
            show_errors()
            selected_label.config(text="")

    ttk.Button(frame, text="Browse Files", style="Home.TButton", command=browse_files).pack(pady=[20, 20], ipadx=10, ipady=10)
    ttk.Button(frame, text="Help", style="Home.TButton", command=show_help_callback).pack(pady=20, ipadx=10, ipady=10)
    ttk.Button(frame, text="About", style="Home.TButton", command=show_about_callback).pack(pady=20, ipadx=10, ipady=10)

    return frame
