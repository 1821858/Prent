from tkinter import *
from tkinter import ttk

# Create main window
root = Tk()
root.title("Prent")

# Get computer screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set window size to 75% of screen dimensions
dynamic_width = int(screen_width * 0.75)
dynamic_height = int(screen_height * 0.75)

# Center the window upon opening
x = int((screen_width - dynamic_width) / 2)
y = int((screen_height - dynamic_height) / 2)

# Set window size dynamically based on screen dimensions
root.geometry(f"{dynamic_width}x{dynamic_height}+{x}+{y}")



frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
root.mainloop()