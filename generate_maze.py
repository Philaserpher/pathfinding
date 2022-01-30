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
    key = random.randint(1, 4)
    old_key = int(str(key))  # quick way to make a copy
    added = False  # pointer to check that we have looped around

    while True:
        # for all of the following if statements we use the random number to
        # choose a direction, and check that the cell in that direction is
        # empty and that we're not at the edge. If such node does not exist,
        # we add one to our key to try the next direction (not true random
        # in case of hugging an edge, but good enough for now)
        # when a valid cell is found, we empty the wall between the cells and
        # return the position of the new cell, otherwise return the same pos

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
