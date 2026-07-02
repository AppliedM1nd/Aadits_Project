import math

class TreeNode:
    def __init__(self, top_left, bottom_right):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.left = None
        self.right = None


dimensions = (10,10)

items = [(1, 3),
         (2, 5),
         (3, 2),
         (1, 1),
         (7, 7),
         (3, 3)
         ]

grid = [['-'] * dimensions[1] for i in range(dimensions[0])]

root = TreeNode((0,0),(9,9))

nodes = []

def tree_packing(next_box):
    found = False
    while not found:
        for item in nodes:
            if item.left == node or item.right == node:
                if (item.bottom_right[0] - item.top_left[0] >= next_box[0] and item.bottom_right[1] - item.top_left[1] >= next_box[1]) or (item.bottom_right[0] - item.top_left[0] >= next_box[1] and item.bottom_right[1] - item.top_left[1] >= next_box[0]):
                    found = True
                    new_node = TreeNode(next_box[0], next_box[1])
                    nodes.append(new_node)
                for node in nodes

