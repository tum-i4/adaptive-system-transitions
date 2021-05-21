"""
a script to visualize a dirt distribution
does not consider time of appearance of the dirt, only outputs one image
"""
import numpy as np
from PIL import Image
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

# initialize task list
tasks = []

# read tasks into task list
file = open("out.txt", "r")
text = file.read()
text_array = text.split(" ")
for triple in text_array[:-1]:
    triple_array = triple[1:-1].split(",")
    # print triple_array
    x = triple_array[0]
    y = triple_array[1]
    tasks.append((int(x), int(y)))

# read map layout
SIZE = 200
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

# empty_cell_count = np.size(np.where(grid_map == 0)) / 2

tasks_map = put_on_map(tasks, np.zeros((SIZE, SIZE)))

# create and save output image
w, h = 200, 200
data = np.zeros((h, w, 3), dtype=np.uint8)
# data[256, 256] = [255, 0, 0]
data[:, :, 0] = tasks_map + grid_map
data[:, :, 1] = grid_map
data[:, :, 2] = grid_map
img = Image.fromarray(data, 'RGB')
img.save('my.png')
img.show()


