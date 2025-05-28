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

frm = Frame(root)
frm.pack(fill = BOTH, expand=True)

# Font settings
header_font = ("Helvetica", 50, "bold")
subheader_font = ("Helvetica", 30)


ttk.Label(frm, text="Welcome to Prent!", font = header_font).pack(pady = [35,0])
ttk.Label(frm, text="To get started, please upload an image or video file.", font = subheader_font).pack(pady = 10)
ttk.Button(frm, text="Browse Files", style = "Home.TButton").pack(pady = [100, 20], ipadx = 10, ipady = 10)
ttk.Button(frm, text="Help", style = "Home.TButton").pack(pady = 20, ipadx = 10, ipady = 10)
ttk.Button(frm, text="About", style = "Home.TButton").pack(pady = 20, ipadx = 10, ipady = 10)

# Button settings
style = ttk.Style()
style.configure("Home.TButton", font=subheader_font)

root.mainloop()