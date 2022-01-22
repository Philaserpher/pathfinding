import pygame
from node import Node
from a_star import a_star_algorithm

SIZE = 1000
ROWS = 50
WINDOW = pygame.display.set_mode((SIZE, SIZE))
pygame.display.set_caption("Maze solver")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


def generate_grid(rows, size):
    grid = []
    cube_size = size//rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, cube_size, rows)
            grid[i].append(node)

    return grid


def draw_grid(window, rows, size):
    cube_size = size // rows
    for i in range(rows):
        pygame.draw.line(window, GREY, (0, i*cube_size), (size, i*cube_size))
        for j in range(rows):
            pygame.draw.line(window, GREY, (j*cube_size, 0),
                             (j*cube_size, size))


def draw(window, grid, rows, size):
    window.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(window)

    draw_grid(window, rows, size)
    pygame.display.update()


def click_cube(position, rows, size):
    cube_size = size//rows
    row = position[0] // cube_size
    column = position[1] // cube_size
    return row, column


def main(window, size, rows):
    grid = generate_grid(rows, size)

    start = None
    end = None

    run = True
    started = False

    while run:
        draw(window, grid, rows, size)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:
                position = pygame.mouse.get_pos()
                row, column = click_cube(position, rows, size)
                node = grid[row][column]
                if not start and node != end:
                    start = node
                    start.set_start()
                elif not end and node != start:
                    end = node
                    end.set_end()
                elif node != end and node != start:
                    node.set_wall()
            elif pygame.mouse.get_pressed()[2]:
                position = pygame.mouse.get_pos()
                row, column = click_cube(position, rows, size)
                node = grid[row][column]
                node.reset()

                if node == start:
                    start = None
                elif node == end:
                    end = None
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_SPACE
                        and not started and start and end):
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)

                    a_star_algorithm(lambda: draw(window, grid, rows, size),
                                     grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = generate_grid(rows, size)

    pygame.quit()


if __name__ == "__main__":
    main(WINDOW, SIZE, ROWS)
