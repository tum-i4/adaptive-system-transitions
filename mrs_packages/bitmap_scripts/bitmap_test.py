"""
script to help test bits and pieces, has no use on its own
"""
from PIL import Image
import numpy as np
import math


def put_on_map(tasks, map):
    """ puts given tasks onto the given map
    where 'tasks' is a list of task tuples (or triples) and 'map' is a matrix """
    for task in tasks:
        x = int(math.floor(task[0]))
        y = int(math.floor(task[1]))
        # print(x, y)
        map[y][x] = 255
        map[y - 1][x] = 255
        map[y + 1][x] = 255
        map[y][x - 1] = 255
        map[y][x + 1] = 255
    return map


SIZE = 200
ALPHA = 9
PUBLISH_FREQUENCY = 1

robot0_loc = (2, 3)
robot1_loc = (2, 5)
radius = 5.0

tasks = [(123, 140), (3, 45), (56, 120)]
scan_request_publisher = None
map_publisher = None
task_publisher = None

f = open("static_map.pgm", "r")
f.readline(), f.readline(), f.readline(), f.readline(),
data = f.readline()

grid_map = np.zeros((SIZE, SIZE))
for row in range(0, SIZE):
    for column in range(0, SIZE):
        pixel = ord(data[row * SIZE + column])
        if pixel <= 250:
            grid_map[row, column] = -1
    # grid_map[row, column] = pixel

obstacles = grid_map.copy()
exploration_counter = grid_map.copy()

empty_cell_count = np.size(np.where(grid_map == 0)) / 2
initial_prob = 1.0 / empty_cell_count
# print empty_cell_count


def initialize_prob(x):
    if x == -1:
        return 0
    else:
        return initial_prob


probability_acc = np.zeros((SIZE, SIZE))
for ind, line in enumerate(grid_map):
    probability_acc[ind] = map(initialize_prob, grid_map[ind])


tasks_map = put_on_map(tasks, np.zeros((SIZE, SIZE)))
w, h = 200, 200
data = np.zeros((h, w, 3), dtype=np.uint8)
# data[256, 256] = [255, 0, 0]
data[:, :, 0] = tasks_map + grid_map
data[:, :, 1] = grid_map
data[:, :, 2] = grid_map
img = Image.fromarray(data, 'RGB')
img.save('my.png')
img.show()
