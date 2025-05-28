from tkinter import *
from tkinter import ttk

def create_home_page(parent, show_help_callback):
    # Create a frame attached to parent
    frame = Frame(parent)

    # Font settings
    header_font = ("Helvetica", 50, "bold")
    subheader_font = ("Helvetica", 30)
    warning_font = ("Helvetica", 15, "italic")

    # Button settings
    style = ttk.Style()
    style.configure("Home.TButton", font=subheader_font)

    ttk.Label(frame, text="Welcome to Prent!", font=header_font).pack(pady=[35, 0])
    ttk.Label(frame, text="To get started, please upload an image or video file.", font=subheader_font).pack(pady=10)

    error_one = ttk.Label(frame, text="Error: Your file is not a valid image or video file.", font=warning_font, foreground='red')
    error_two = ttk.Label(frame, text="Acceptable file extensions include .jpg, .jpeg, .png, .bmp, .tiff, .tif, and .mp4.", font=warning_font, foreground='red')

    ttk.Button(frame, text="Browse Files", style="Home.TButton").pack(pady=[20, 20], ipadx=10, ipady=10)
    ttk.Button(frame, text="Help", style="Home.TButton", command=show_help_callback).pack(pady=20, ipadx=10, ipady=10)
    ttk.Button(frame, text="About", style="Home.TButton").pack(pady=20, ipadx=10, ipady=10)

    # example function to show errors (not called yet)
    def show_errors():
        error_one.pack(pady=10)
        error_two.pack(pady=10)

    return frame