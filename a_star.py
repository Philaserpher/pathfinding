from queue import PriorityQueue
import pygame

# based on https://www.youtube.com/watch?v=JtiK0DOeI4A

# define the heuristic function, which is used to determine how far away from
# the end a node is
# in this case using Manhattan distance (abs(delta x) + abs(delta y))


def heuristic(point, target):  # define the heuristic function
    return abs(point[0]-target[0]) + abs(point[1] - target[1])


def a_star_algorithm(draw, grid, start, end):
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

# once a path is found, we build it by marking every node in visited as path


def build_path(visited, current, draw):
    while current in visited:
        current = visited[current]
        current.set_path()
        draw()
