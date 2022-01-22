import pygame
import math
import time
from queue import PriorityQueue

SIZE = 1000
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


class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x_position = row*width
        self.y_position = col*width
        self.width = width
        self.total_rows = total_rows
        self.colour = WHITE
        self.neighbours = []

    def get_position(self):
        return self.row, self.col

    def is_visited(self):
        return self.colour == RED

    def is_open(self):
        return self.colour == GREEN

    def is_wall(self):
        return self.colour == BLACK

    def is_start(self):
        return self.colour == PURPLE

    def is_end(self):
        return self.colour == ORANGE

    def reset(self):
        self.colour = WHITE

    def set_start(self):
        self.colour = PURPLE

    def set_end(self):
        self.colour = ORANGE

    def set_path(self):
        self.colour = TURQUOISE

    def set_visited(self):
        self.colour = RED

    def set_open(self):
        self.colour = GREEN

    def set_wall(self):
        self.colour = BLACK

    def draw(self, window):
        pygame.draw.rect(window, self.colour,
                         (self.x_position, self.y_position,
                          self.width, self.width))

    def update_neighbours(self, grid):
        self.neighbours = []

        if self.row < self.total_rows - 1 and not (grid[  # DOWN
                self.row + 1][self.col].is_wall()):
            self.neighbours.append(grid[self.row + 1][self.col])

        if self.row > 0 and not (grid[  # UP
                self.row - 1][self.col].is_wall()):
            self.neighbours.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not (grid[  # RIGHT
                self.row][self.col + 1].is_wall()):
            self.neighbours.append(grid[self.row][self.col + 1])

        if self.col > 0 and not (grid[  # RIGHT
                self.row][self.col - 1].is_wall()):
            self.neighbours.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def heuristic(point, target):
    return abs(point[0]-target[0]) + abs(point[1] - target[1])


def build_path(visited, current, draw):
    while current in visited:
        current = visited[current]
        current.set_path()
        draw()


def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    previous_node = {}
    cost = {node: float("inf") for row in grid for node in row}
    cost[start] = 0
    total_cost = {node: float("inf") for row in grid for node in row}
    total_cost[start] = heuristic(start.get_position(), end.get_position())

    open_set_hash = {start}

    while not open_set.empty():
        time.sleep(0.001)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            build_path(previous_node, end, draw)
            start.set_start()
            end.set_end()
            return True

        for neighbour in current.neighbours:
            temp_cost = cost[current] + 1

            if temp_cost < cost[neighbour]:
                previous_node[neighbour] = current
                cost[neighbour] = temp_cost
                total_cost[neighbour] = temp_cost + \
                    heuristic(neighbour.get_position(), end.get_position())
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((total_cost[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.set_open()  # open = discovered
        draw()
        if current != start:
            current.set_visited()

    return False


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


def main(window, size):
    ROWS = 50
    grid = generate_grid(ROWS, size)

    start = None
    end = None

    run = True
    started = False

    while run:
        draw(window, grid, ROWS, size)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:
                position = pygame.mouse.get_pos()
                row, column = click_cube(position, ROWS, size)
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
                row, column = click_cube(position, ROWS, size)
                node = grid[row][column]
                node.reset()

                if node == start:
                    start = None
                elif node == end:
                    end = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:

                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)

                    algorithm(lambda: draw(window, grid, ROWS, size),
                              grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = generate_grid(ROWS, size)

    pygame.quit()


main(WINDOW, SIZE)
