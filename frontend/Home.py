from tkinter import *
from tkinter import ttk


def create_home_page(parent, browse_callback, show_help_callback, show_about_callback, state=None):
    frame = Frame(parent)

    header_font = ("Helvetica", 50, "bold")
    subheader_font = ("Helvetica", 30)
    warning_font = ("Helvetica", 15, "italic")

    style = ttk.Style()
    style.configure("Home.TButton", font=subheader_font)

    ttk.Label(frame, text="Welcome to Prent!", font=header_font).pack(pady=[35, 0])
    ttk.Label(frame, text="To get started, please upload an image or video file.", font=subheader_font).pack(pady=10)

    ttk.Button(
        frame,
        text="Browse Files",
        style="Home.TButton",
        command=browse_callback
    ).pack(pady=[20, 20], ipadx=10, ipady=10)

    ttk.Button(
        frame,
        text="Help",
        style="Home.TButton",
        command=show_help_callback
    ).pack(pady=20, ipadx=10, ipady=10)

    ttk.Button(
        frame,
        text="About",
        style="Home.TButton",
        command=show_about_callback
    ).pack(pady=20, ipadx=10, ipady=10)

    if state and state.file_path:
        ttk.Label(frame, text=f"Current file: {state.file_path}", font=("Helvetica", 12)).pack(pady=10)

    return frame