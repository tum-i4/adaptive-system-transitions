"""
generates tasks and saves them to a text file
tasks are generated uniformly randomly and are never on obstacles
"""
import numpy as np
import random
import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
from skimage.draw import line,circle,ellipse,circle_perimeter
from sklearn.preprocessing import normalize




def import_gridmap():
    # import gridmap
    img = mpimg.imread('_tmp.pgm') 

    data = np.asarray(img)
    SIZE = int(data.shape[0])

    # read map layout

    grid_map = np.zeros((SIZE,SIZE))

    for row in range(0, SIZE):
        for column in range(0, SIZE):
            pixel = data[row][column]
            if pixel <= 250:
                grid_map[row, column] = 1

    return grid_map
"""
obstacles = []
grid_map = np.array([
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,1,1,1,0,0,0,0],
    [0,0,0,1,1,1,0,0,0,0],
    [0,0,0,1,1,1,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0],
])
SIZE = int(10)
#obstacles.append(4,4)
#obstacles.append(5,4)
for row in range(0, SIZE):
    for column in range(0, SIZE):
        pixel = grid_map[row][column]
        if pixel >= 0.5:
            obstacles.append((row,column))
"""
def generate_exploration_tasks(NO_OF_TASKS_U,NO_OF_TASKS_G,radius,obstacle_treshold,grid_map):
    SIZE = int(grid_map.shape[0])
    obstacles = []
    Visualization = np.zeros((SIZE,SIZE))
    for row in range(0, SIZE):
        for column in range(0, SIZE):
            pixel = grid_map[row][column]
            if pixel >= 0.5:
                obstacles.append((row,column))
                Visualization[row, column] = -1
    
    Exploration_task_likelihood = np.zeros((SIZE,SIZE))
    print("Exploration task sampler is processing...")
    for obstacle in obstacles:
        treated_buffer = [] 
        
        for i in range(1, radius+1):
            rr, cc = circle_perimeter(int(math.ceil(obstacle[0])), int(math.ceil(obstacle[1])), i, method='andres', shape=None)
            circle_list = []
            for a in range (len(rr)):
                circle_list.append((rr[a],cc[a]))
            circle_list = list(set(circle_list))

            # Delete everything not on the map
            to_remove = []
            for tup in circle_list:
                if tup[0] < 0 or tup[1] < 0 or tup[0] >= SIZE or tup[1] >= SIZE:
                    to_remove.append(tup)
            for rem in to_remove:    
                circle_list.remove(rem)
                
            
            to_treat = [elem for elem in circle_list if elem not in treated_buffer]
            # Check if the obstacle is a large obstacle which has no priority
            neighboring_obstacle_counter = 0
            if i < 3:
                for pixel in circle_list:
                    if grid_map[pixel[0],pixel[1]] > 0.5:
                        neighboring_obstacle_counter += 1
            if neighboring_obstacle_counter > obstacle_treshold:
                break
            # Generate Exploration task liklihood
            for pixel in to_treat:
                if grid_map[pixel[0],pixel[1]] < 0.5:      # circle is not on an obstacle or over the map
                    Exploration_task_likelihood[pixel[0],pixel[1]] += (radius - i)/radius 
            treated_buffer = treated_buffer + to_treat



    total_tasks_created = 0

    tasks_created = 0
    Exploration_tasks = []
    text = ''

    normalized_Exploration_task_likelihood = np.interp(Exploration_task_likelihood, (Exploration_task_likelihood.min(), Exploration_task_likelihood.max()), (0, +1))
    # Generate Exploration tasks according to importance
    while tasks_created < NO_OF_TASKS_G:

        x = int(random.randrange(SIZE- 1)) 
        y = int(random.randrange(SIZE- 1)) 
            # check if the Exploration task is close to an obstacle 
        if grid_map[y][x] != 1 and grid_map[y-1][x] != 1 and grid_map[y+1][x] != 1 and grid_map[y][x-1] != 1 and grid_map[y][x+1] != 1 and grid_map[y-1][x-1] != 1 and grid_map[y-1][x+1] != 1 and grid_map[y+1][x-1] != 1 and grid_map[y+1][x+1] != 1:
            
            placing_treshold = random.random()
            if normalized_Exploration_task_likelihood[y][x] > placing_treshold:
                grid_map[y][x] = 1        # Marking the exploration task as obstacle prevents duplicates
                Visualization [y][x] = 1
                # text += '('
                #text += str(x) + ',' + str(y) + ',' + str(int(time))
                text += str(x) + ',' + str(y) #+ ',0'
                text += '\n'
                tasks_created += 1
                total_tasks_created += 1
                Exploration_tasks.append((x,y))

    tasks_created = 0
    # Placing exploration tasks randomly
    while tasks_created < NO_OF_TASKS_U:

        x = int(random.randrange(SIZE- 1)) 
        y = int(random.randrange(SIZE- 1)) 

            # check if the Exploration task is close to an obstacle 
        if grid_map[y][x] != 1 and grid_map[y-1][x] != 1 and grid_map[y+1][x] != 1 and grid_map[y][x-1] != 1 and grid_map[y][x+1] != 1 and grid_map[y-1][x-1] != 1 and grid_map[y-1][x+1] != 1 and grid_map[y+1][x-1] != 1 and grid_map[y+1][x+1] != 1:            
            grid_map[y][x] = 1        # Marking the exploration task as obstacle prevents duplicates
            Visualization [y][x] = 1
            # text += '('
            #text += str(x) + ',' + str(y) + ',' + str(int(time))
            text += str(x) + ',' + str(y) #+ ',0'
            text += '\n'
            tasks_created += 1
            total_tasks_created += 1
            Exploration_tasks.append((x,y))
    print("Exploration taks sampler is finished")
    return text, Exploration_task_likelihood, Visualization

"""
# Uniform distributed tasks
NO_OF_TASKS_U = 1000  # total number of exploration tasks to be generated randomly
NO_OF_TASKS_G = 0    # number of exploration tasks to be generated according to importance
radius = 30           # Radius of importance around the obstacles
obstacle_treshold = 3  # Determines the number of neigeighbors needed in a obstacle to not be considered. Otherwise large obstacles would have a high importance

grid_map = import_gridmap()
text, Exploration_task_likelihood, Visualization = generate_exploration_tasks(NO_OF_TASKS_U,NO_OF_TASKS_G,radius,obstacle_treshold,grid_map)
img = Image.fromarray(Exploration_task_likelihood)
img = img.convert('RGB')
img.save('my.png')
img.show()
print("Exploration task sampler is finished :)")


# save output to txt file
file = open("out.txt", "w")
file.write(text)
file.close()

# visualize the distribution
#plt.imshow(data)
plt.imshow(Visualization)
plt.show()
"""