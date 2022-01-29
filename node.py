import pygame

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

    def is_empty(self):
        return self.colour == WHITE

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
