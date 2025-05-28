from tkinter import *
from tkinter import ttk
from Home import create_home_page
from Help import create_help_page

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

frame = Frame(root)
frame.pack(fill = BOTH, expand=True)

def show_home():
    for widget in frame.winfo_children():
        widget.destroy()
    home_frame = create_home_page(frame, show_help)
    home_frame.pack(fill=BOTH, expand=True)

def show_help():
    for widget in frame.winfo_children():
        widget.destroy()
    help_frame = create_help_page(frame)
    help_frame.pack(fill=BOTH, expand=True)


show_home()

root.mainloop()