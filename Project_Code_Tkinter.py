import tkinter as tk
import Project_Code_File4 as network

root = tk.Tk()
root.title("Network Simulation")
root.geometry("1000x800")
canvas = tk.Canvas(root, bg="white")
canvas.pack() # positions canvas in window
node_position = {}


def generate_positions():
    for index, node in enumerate(network.nodes):
        row = index // 5
        column = index % 5

        x = 100 * column + 100
        y = 100 * row + 80

        node_position[node] = (x, y)

def draw_network():
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

network.create_test_network()
generate_positions()
draw_network()

root.mainloop()






