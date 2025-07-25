from tkinter import *
from tkinter import ttk

def create_about_page(parent, show_home_callback):
    main_frame = Frame(parent)
    # Font settings
    header_font = ("Helvetica", 50, "bold")
    version_font = ("Helvetica", 25, "bold")
    body_font = ("Helvetica", 18)

    # Button settings
    style = ttk.Style()
    style.configure("Home.TButton", font=body_font)

    about_text = (
        "Prent is an image and video editing software that uses OpenCV to process files and apply effects.\n\n"
        "Currently, the available effects include polygonize, cartoon, and sketch, but stay tuned for more effects to come.\n\n"
        "Prent was made by users Curiousfish and Grackfish as a personal project. View our growing GitHub repository here!"
    )

    ttk.Label(main_frame, text="About", font=header_font).pack(pady=[35, 0])
    ttk.Label(main_frame, text="Version 1.0", font=version_font).pack()

    body_frame = Frame(main_frame)
    body_frame.pack(fill=X)
    ttk.Label(body_frame, text=about_text, wraplength=1050, justify=LEFT, font=body_font).pack(pady=35)

    ttk.Button(main_frame, text="Back", command=show_home_callback, style="Home.TButton").pack(ipadx=10, ipady=10)

    return main_frame