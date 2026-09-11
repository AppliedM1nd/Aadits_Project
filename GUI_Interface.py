import tkinter as tk
window = tk.Tk()
window.geometry("500x500")

def on_drag_start(event):
    event.widget.startX = event.x
    event.widget.startY = event.y

def on_move_drag(event):
    x = event.widget.winfo_x() + event.x - event.widget.startX
    y = event.widget.winfo_y() + event.y - event.widget.startY
    event.widget.place(x=x, y=y)

all_connected = False



label = tk.Label(window, text="Network Simulation")
label = tk.Label(window, text=all_connected)

label.bind("<ButtonPress>", on_drag_start)


label.pack()


window.mainloop()