"""
Reads a distribution text file and creates image files to animate the dirt distribution.
Images are saved in the folder 'Animation' in the same directory.
"""

from PIL import Image
import numpy as np
import math

def read_txt(path):
    """ given the path to the text file, reads a string of tasks
    returns an UNsorted list of tasks 
    where each task is [x_coordinat, y_coortinate, # of sample] """
    file = open(str(path), 'r')
    lines = file.readlines()
    lines = [line[:-1] if line[-1:]=='\n' else line for line in lines]
    # print(lines)
    tuples = []
    for line in lines:
        line = line.split(',')
        tuples.append(line)
        # print(line)

    floatstuple = []
    
    for item in tuples:
        temp = []
        for entry in item:
            temp.append(float(entry))
        floatstuple.append(temp)
    return(floatstuple)

def getKey(item):
    return item[2]


def deterministic_sample_list(tasktxt):
    """ given the path to the text file, reads a string of tasks
    returns a sorted list of tasks 
    where each task is [x_coordinat, y_coortinate, # of sample] """
    determinisitic_task_list = read_txt(tasktxt)               # Insert path from txt file
    determinisitic_task_list.sort(key=getKey)
    return determinisitic_task_list


def mult(matrix, constant):
    """ multiplies each element of a given matrix by the given constant """
    # need to copy to a new matrix to operate, or the original matrix is also changed
    new_matrix = np.array(matrix).copy().tolist()
    for i, row in enumerate(matrix):
        for j, element in enumerate(row):
            new_matrix[i][j] = int(new_matrix[i][j] * constant)
            if new_matrix[i][j] > 255:
                new_matrix[i][j] = 255
    return new_matrix

def put_on_map_tasks(tasks, map):
    """ puts given tasks onto the given map
    where 'tasks' is a list of task tuples (or triples) and 'map' is a matrix """
    for task in tasks:
        x = int(math.floor(task[0]))
        y = int(math.floor(task[1]))
        # print(x, y)
        map[y][x] = 1
        map[y - 1][x] = 1
        map[y + 1][x] = 1
        map[y][x - 1] = 1
        map[y][x + 1] = 1
    return map

SIZE = 200  # size of the map

f = open("static_map.pgm", "r")    # map image file to read
f.readline(), f.readline(), f.readline(), f.readline(),
data = f.readline()

# create the grid map to add the dirt and obstacles
grid_map = np.zeros((SIZE, SIZE))
for row in range(0, SIZE):
    for column in range(0, SIZE):
        pixel = ord(data[row * SIZE + column])
        if pixel <= 250:
            grid_map[row, column] = -1
    # grid_map[row, column] = pixel

obstacles = grid_map.copy()

task_list = deterministic_sample_list('/home/defaultuser/catkin_ws/src/t4-mrs_packages/bitmap_scripts/out.txt')
working_list = np.array(task_list).copy().tolist()
time = 0

# need rgb layers to create an image
data1 = np.zeros((SIZE, SIZE, 3))
data1[:, :, 0] = obstacles
data1[:, :, 1] = obstacles
data1[:, :, 2] = obstacles
data1 = data1.astype(np.uint8, casting='unsafe')


while working_list:
    
    recent_tasks = [task for task in working_list if task[2] == time]

    for task in recent_tasks:
        working_list.remove(task)

    recent_tasks = [task[:-1] for task in recent_tasks]    

    undiscovered_tasks_map = put_on_map_tasks(recent_tasks, np.zeros((SIZE, SIZE)))
    undiscovered_tasks_map = mult(undiscovered_tasks_map, 255)
    undiscovered_tasks_map = np.array(undiscovered_tasks_map).astype(np.uint8, casting='unsafe')


    data1[:, :, 0] += undiscovered_tasks_map
    # data1[:, :, 1] += undiscovered_tasks_map
    # data1[:, :, 2] += undiscovered_tasks_map
    
    data1 = data1.astype(np.uint8, casting='unsafe')

    time += 1
    
    # save one image for each time
    img = Image.fromarray(data1, 'RGB')
    img.save('/home/defaultuser/catkin_ws/src/t4-mrs_packages/bitmap_scripts/animation/'+str(time)+'.png')
    #img.show()
