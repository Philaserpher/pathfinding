import pygame
from node import Node
from a_star import a_star_algorithm
from generate_maze import generate_maze

SIZE = 1000
ROWS = 100
WINDOW = pygame.display.set_mode((SIZE, SIZE))
pygame.display.set_caption("Maze solver")

WHITE = (255, 255, 255)
GREY = (128, 128, 128)


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


def main(window, grid, size, rows):

    start = None
    end = None

    run = True
    started = False
    step_drawings = True

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
                if event.key == pygame.K_f:
                    step_drawings = not step_drawings
                if (event.key == pygame.K_SPACE
                        and not started and start and end):
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)

                    a_star_algorithm(lambda: draw(window, grid, rows, size),
                                     grid, start, end, step_drawings)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = generate_grid(rows, size)

                if event.key == pygame.K_g:
                    grid, start, end = generate_maze(grid, rows)
    pygame.quit()


if __name__ == "__main__":
    GRID = generate_grid(ROWS, SIZE)
    main(WINDOW, GRID, SIZE, ROWS)
