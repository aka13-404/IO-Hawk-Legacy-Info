# Import the required libraries
from tkinter import *
from tkinter import ttk

# Create an instance of tkinter frame or window
win = Tk()

# Set the size of the window
win.geometry("700x350")

running = True

# Define a function to print the text in a loop
def print_text():
   if running:
      print("Hello World")

   win.after(1000, print_text)

# Define a function to start the loop
def on_start():
   global running
   running = True

# Define a function to stop the loop
def on_stop():
   global running
   running = False

canvas = Canvas(win, bg="skyblue3", width=600, height=60)
canvas.create_text(150, 10, text="Click the Start/Stop to execute the Code", font=('', 13))
canvas.pack()

# Add a Button to start/stop the loop
start = ttk.Button(win, text="Start", command=on_start)
start.pack(padx=10)

stop = ttk.Button(win, text="Stop", command=on_stop)
stop.pack(padx=10)

# Run a function to print text in window
win.after(1000, print_text)
