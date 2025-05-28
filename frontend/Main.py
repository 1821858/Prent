from tkinter import *
from tkinter import ttk

# Create main window
root = Tk()
root.title("Prent")

# Get computer screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Dynamic window sizing and centering
dynamic_width = int(screen_width * 0.75)
dynamic_height = int(screen_height * 0.75)
x = int((screen_width - dynamic_width) / 2)
y = int((screen_height - dynamic_height) / 2)
root.geometry(f"{dynamic_width}x{dynamic_height}+{x}+{y}")

frm = Frame(root)
frm.pack(fill = BOTH, expand=True)

# Font settings
header_font = ("Helvetica", 50, "bold")
subheader_font = ("Helvetica", 30)
warning_font = ("Helvetica", 15, "italic")

# Button settings
style = ttk.Style()
style.configure("Home.TButton", font=subheader_font)

ttk.Label(frm, text="Welcome to Prent!", font = header_font).pack(pady = [35,0])
ttk.Label(frm, text="To get started, please upload an image or video file.", font = subheader_font).pack(pady = 10)
error_one = ttk.Label(frm, text="Error: Your file is not a valid image or video file.", font = warning_font, foreground = 'red')#.pack(pady = 10)
error_two = ttk.Label(frm, text="Acceptable file extensions include .jpg, .jpeg, .png, .bmp, .tiff, .tif, and .mp4.", font = warning_font, foreground = 'red')#.pack(pady = 10)
ttk.Button(frm, text="Browse Files", style = "Home.TButton").pack(pady = [20, 20], ipadx = 10, ipady = 10)
ttk.Button(frm, text="Help", style = "Home.TButton").pack(pady = 20, ipadx = 10, ipady = 10)
ttk.Button(frm, text="About", style = "Home.TButton").pack(pady = 20, ipadx = 10, ipady = 10)

def show_errors():
    error_one.pack(pady=10)
    error_two.pack(pady=10)

root.mainloop()