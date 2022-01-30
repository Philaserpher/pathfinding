import random

# growing tree algorithm


def generate_maze(window, grid, rows, size):
    cells_pos = []

    for row in grid:
        for node in row:
            node.set_wall()
    pos = (random.randint(1, (rows-2)/2)*2-1,
           random.randint(1, (rows-2)/2)*2-1)
    node = grid[pos[0]][pos[1]]
    node.reset()
    cells_pos.append(pos)
    while cells_pos:
        pos = get_neighbour(cells_pos[-1], grid, rows)
        node = grid[pos[0]][pos[1]]
        if not node.is_empty():
            node.reset()
            cells_pos.append(pos)
            continue
        cells_pos.pop()
    start = grid[1][1]
    start.set_start()
    end = grid[-3][-3]
    end.set_end()
    return(grid, start, end)


def get_neighbour(pos, grid, rows):
    key = random.randint(1, 4)
    old_key = int(str(key))
    added = False
    while True:

        if (key == 1 and pos[1] > 2 and
                not grid[pos[0]][pos[1]-2].is_empty()):
            grid[pos[0]][pos[1]-1].reset()
            return((pos[0], pos[1]-2))
        elif (key == 2 and pos[0] < rows-3 and
              not grid[pos[0]+2][pos[1]].is_empty()):
            grid[pos[0]+1][pos[1]].reset()
            return((pos[0]+2, pos[1]))
        elif (key == 3 and pos[1] < rows-3 and
              not grid[pos[0]][pos[1]+2].is_empty()):
            grid[pos[0]][pos[1]+1].reset()
            return((pos[0], pos[1]+2))
        elif (key == 4 and pos[0] > 2 and
              not grid[pos[0]-2][pos[1]].is_empty()):
            grid[pos[0]-1][pos[1]].reset()
            return((pos[0]-2, pos[1]))

        if key < 5:
            key += 1
            added = True
        else:
            key = 1
        if key == old_key and added:
            return(pos)
