import tkinter as tk
import Project_Code_File4 as network

root = tk.Tk()
root.title("Network Simulation")
root.geometry("1000x800")
canvas = tk.Canvas(root, bg="white")
canvas.pack(fill="both", expand=True) # positions canvas in window and allows it to fill all available space in x and y and to take up extra space in window
node_position = {}
selected_node = None


def generate_positions():
    for index, node in enumerate(network.nodes):
        row = index // 5
        column = index % 5

        x = 100 * column + 100
        y = 100 * row + 80

        node_position[node] = (x, y)

def draw_network():
    canvas.delete("all")
    for node_name, node in network.nodes.items():
        for neighbour, distance in node.connections:
            if node_name < neighbour:
                x1, y1 = node_position[node_name]
                x2, y2 = node_position[neighbour]

                canvas.create_line(x1, y1, x2, y2, width = 2, fill="black")

    for node_name, node in network.nodes.items():
        x,y = node_position[node_name]

        canvas.create_oval(x-25, y-25, x+25, y+25, fill="red")
        canvas.create_text(x, y, text=node_name)  #anchor=tk.W

def select_node(event):
    global selected_node
    for node_name, (x,y) in node_position.items():
        distance = ((event.x - x)**2 + (event.y - y)**2)**(0.5)
        if distance <= 25:
            selected_node = node_name

def move_node(event):
    if selected_node is not None:
        node_position[selected_node] = event.x, event.y
        draw_network()

def release_node(event):
    global selected_node
    if selected_node is not None:
        selected_node = None

def display_packets(event):
    global selected_node

network.create_test_network()
generate_positions()
draw_network()

canvas.bind("<Button-1>", select_node)
canvas.bind("<B1-Motion>", move_node)
canvas.bind("<ButtonRelease-1>", release_node)

sidebar = tk.Frame(root, bg="blue", width=100, height=800)
sidebar.pack(fill="both", expand=True, side = "left")
sidebar_label = tk.Label(sidebar, text="Menu")
sidebar_label.pack(side="left")
#canvas.create_window(150, 100, window=sidebar)
root.mainloop()






