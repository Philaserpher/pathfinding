import random

# growing tree algorithm for maze generation
# explained in detail in readme


def generate_maze(grid, rows):

    cells_pos = []  # list of the position of cells in consideration

    for row in grid:  # set the entire grid to be walls
        for node in row:
            node.set_wall()

    pos = (random.randint(1, (rows-2)/2)*2-1,
           random.randint(1, (rows-2)/2)*2-1)

    node = grid[pos[0]][pos[1]]
    node.reset()  # choose a random position, and clear the node
    cells_pos.append(pos)  # add node to list of nodes considered

    while cells_pos:
        # choose a random neighbour of the last node in the list
        pos = get_neighbour(cells_pos[-1], grid, rows)
        node = grid[pos[0]][pos[1]]
        # if the node has not been considered already (therefore it is path)
        if not node.is_empty():
            node.reset()  # clear node
            cells_pos.append(pos)  # add to considered list
            continue
        cells_pos.pop()
        # if there are no empty neighbours, remove node from list
    start = grid[1][1]
    start.set_start()
    end = grid[-3][-3]
    end.set_end()  # set start and ends on opposite corners
    return(grid, start, end)


def get_neighbour(pos, grid, rows):  # used to randomly select neighbours
    sides_left = 3
    sides = [1, 2, 3, 4]
    key = random.randint(0, sides_left)

    while True:

        key = sides[key]
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
        sides.remove(key)
        if not sides:
            return pos
        sides_left -= 1
        key = random.randint(0, sides_left)
