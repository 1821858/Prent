from tkinter import *
from tkinter import ttk

def create_help_page(parent, show_home_callback):
    main_frame = Frame(parent)
    # Font settings
    header_font = ("Helvetica", 50, "bold")
    body_font = ("Helvetica", 18)

    # Button settings
    style = ttk.Style()
    style.configure("Home.TButton", font=body_font)

    help_text = (
        "To get started, upload an image or video file. Keep in mind that the larger your file size, "
        "the longer it will take to process. Acceptable file types include .jpg, .jpeg, .png, .bmp, .tiff, "
        ".tif, and .mp4.\n\nNext, choose the effect that you would like to apply to your file. If you choose "
        "the polygonize effect, you have the option to customize the number of polygons and amount of color "
        "reduction in your final product. Keep in mind that the larger these values are, the longer it will "
        "take to process. If you don’t know what effects or values you want to apply to your file yet, don’t "
        "worry! You will have the opportunity to preview and adjust them later.\n\nFinally, a preview will be "
        "generated and you will have the option to download the file. If you don’t like how it looks, you "
        "will have the option to adjust effects and values, or upload a completely new file to edit."
    )

    ttk.Label(main_frame, text="Help", font=header_font).pack(pady=[35, 0])

    body_frame = Frame(main_frame)
    body_frame.pack(fill=X)
    ttk.Label(body_frame, text=help_text, wraplength=1050, justify=LEFT, font=body_font).pack(pady=25)

    ttk.Button(main_frame, text="Back", command=show_home_callback, style="Home.TButton").pack(ipadx=10, ipady=10)

    return main_frame