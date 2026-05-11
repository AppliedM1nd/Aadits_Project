def place_item(item, pos, grid, letters, k):
    for i in range(pos[0], pos[0] + item[0]):
        for j in range(pos[1], pos[1] + item[1]):
            grid[i][j] = letters[k]
    return grid


def verify_placement(item, pos, grid):
    if pos[0] + item[0] - 1 <= dimensions[0] - 1 and pos[1] + item[1] - 1 <= dimensions[1] - 1:
        empty = True
        for i in range(pos[0], pos[0] + item[0]):
            for j in range(pos[1], pos[1] + item[1]):
                if grid[i][j] != '-':
                    empty = False
        if empty:
            return True
    return False


def place_next_item(grid, items, current, placed_items, letters, k):
    row = 0
    col = 0
    found = False
    end = False
    while not found and not end:
        if grid[row][col] == '-':
            temp_pos = (row, col)
            result = verify_placement(items[current], temp_pos, grid)
            if result:
                found = True
                grid = place_item(items[current], temp_pos, grid, letters, k)
                placed_items.append(items[current])
        if col < len(grid[0]) - 1:
            col += 1
        elif row == len(grid) - 1:
            end = True
            print('No space for this item:', items[current])
        else:
            row += 1
            col = 0
    current += 1
    if current < len(items):
        k += 1
        place_next_item(grid, items, current, placed_items, letters, k)
    return placed_items


placed_items = []

dimensions = (10, 10)

items = [(1, 3),
         (2, 5),
         (3, 2),
         (1, 1),
         (7, 7),
         (3, 3),
         (2,2)
         ]

letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
k = 0

grid = [['-'] * dimensions[1] for i in range(dimensions[0])]

placed_items = place_next_item(grid, items, 0, placed_items, letters, k)

# for row in grid:
#    print(row)

for row in grid[::-1]:
    print('  '.join(f'{col:>3}' for col in row))