import random

# growing tree algorithm


def generate_maze(grid, rows, size):
    cells = []

    for row in grid:
        for node in row:
            node.set_wall()
    pos = (random.randint(1, (rows-2)/2)*2-1,
           random.randint(1, (rows-2)/2)*2-1)
    node = grid[pos[0]][pos[1]]
    node.reset()
    cells.append(node)
    for i in range(0, 10):
        node = get_neighbour(pos)
        node = grid[pos[0]][pos[1]]
        node.reset()
        cells.append(node)

    return(grid)


def get_neighbour(pos):
    pass
