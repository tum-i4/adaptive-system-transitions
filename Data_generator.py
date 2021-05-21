#!/usr/bin/env python3
import os
import zmq
import time
import psutil
import subprocess
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import random
from netpbmfile import imwrite
import signal
import json
from skopt import Optimizer
from skopt.plots import plot_objective


import mrs_simulation.Bayes_Opt as opt
import task_sampler.task_sampler as ts
import room_generator.room_generator as rg
import Exploration_task_sampler.Exploration_task_sampler as ets

Activate_map_generator = False          #If activated automatic maps are generated. If not, maps are taken form Maps folder
###########################################################Parameter################################################################
#******* Data generation parameter *****************

No_of_maps = 5                  # Number of maps which are being processed
No_of_task_distr = 5            # Number of different task distributions for each map. Total experiments No_of_maps*No_of_task_distr

#***********Room parameter***********:
map_length=400                      # number of pixle the quadratic map is in size
occupancy=0.6                       # How much of the map is occupied by rooms or obstacles (1 = full occupancy)
max_size_obstacle=120               # Maximum size of the obstacles, the largest shape exist is 200*200


#************ Exploration task smapler parameter*******************
NO_OF_TASKS_U = 1000  # total number of exploration tasks to be generated randomly
NO_OF_TASKS_G = 0     # number of exploration tasks to be generated according to importance
radius = 1           # Radius of importance around the obstacles
obstacle_treshold = 3  # Determines the number of neigeighbors needed in a obstacle to not be considered. Otherwise large obstacles would have a high importance


#************** Task sampler parameter ***************************
### Note that the time measure is iterations in the simulator node
# Gaussian tasks:
manual_tasks = False    # If true, manual defined distributions are used (Always sampled from same parameter)
maximum_time = 5400 # Longest time when the last task is allowed to be taskd
maximum_time_intervall = 80 # Maximum timine between the tasks are sampled in one spot
maximum_no_of_tasks = 180  # Maximum number of taks in one task distribution
max_task_per_t = 10       # Maximum number of tasks at a time
number_of_gauss_tasks_min = 400  #Minimum total number of tasks drawn by all gaussians combined. (It will be drawn slightly more than that. Its the break up point)
number_of_gauss_tasks_max = 760  #Maximum total number of tasks drawn by all gaussians combined. (It will be drawn slightly more than that. Its the break up point)
max_equal_distriburion_number =  3    #Maximum Number of equal distributions at different times

max_variance = 30

# Uniform distributed tasks
number_of_uniform_tasks_min = 170  # Minimal total number of tasks to be generated
number_of_uniform_tasks_max = 420  # Maximal total number of tasks to be generated


#***********Optimization parameter***********:
num_of_solution_samples = 4                            # Determines the number of solution samples which are executed during one iteration
num_of_parrallel_executed_solution_samples = 2          # Determines the number of solution samples, which are executed in parrallel.
Number_iter_next_sample = 6000                          # Determines how many iterations each sample solution is supposed to have (simulation lenth)
Bayes_iterations = 10                                   # Determines the number of iterations of the Bayesian optimization. One iteration processes num_of_solution_samples many samples
Initial_random_samples = 60                           # Determines the number of random sampled points to initialize the surrogate model of the bayesian approach
Maximize = False                                       # If false, the algorithm searches the minima, if true, the perfromance measure is negated resulting in serching the maximum. Note that the performance values are now all negative
#***************** Parameter for Data management ******************


#########################################################################################################################################

def save_as_pgm(path_and_file_name, data):
    data[np.where(data>0.5)] = 255
    imwrite(path_and_file_name, data.astype(int))

def save_as_png(path_and_file_name,data):
    img = Image.fromarray(data)
    img = img.convert('RGB')
    img.save(path_and_file_name)

def save_as_txt(path_and_file_name,txt):
    file = open(path_and_file_name, "w")
    file.write(txt)
    file.close()

def visualize(data):
    plt.imshow(data)
    plt.show()

def save_json(save_data_folder,result):
    #Save the reult as Json file
    print("saving JSON")
    with open(str(save_data_folder)+"_Json_"+str(Map_ID)+".txt", 'w') as jsonfile:
        json.dump(result, jsonfile)
    
def save_Bayesian_raw_data(save_data_folder,result,all_f_val,all_param):    
    #Save the sample points as raw data
    print("saving Bayesian_raw_data")
    task_file = open(save_data_folder, "w+")
    i = 0
    task_file.write(str(result.x) + '\n')
    for array in all_param:
        task_file.write(str(all_f_val[i]) + ";" + str(array) + '\n')
        i = i + 1
    task_file.close()

def save_convergence_plot_data(save_data_folder,plot_f_val,start_time):   
    #save convergence plot
    print("saving convergence_plot_data")
    ConvergenceFile = open(save_data_folder , "w+")
    print("PLOT_F_VAL: " + str(plot_f_val))
    ConvergenceFile.write("Process finished in %s seconds" % (time.time() - start_time) +'\n')
    for sample in plot_f_val:
        ConvergenceFile.write(str(sample) +'\n')
    ConvergenceFile.close()

def save_convergence_plot_figure(save_data_folder,plot_f_val):  
    x = np.linspace(0, len(plot_f_val), len(plot_f_val))
    plt.plot(x, plot_f_val)  
    plt.xlabel('Iteration')  
    plt.ylabel('Performance')  
    plt.savefig(save_data_folder) 

def save_objective_figure(save_data_folder, result, all_param):
    print("saving objective_figure")
    plt.clf()
    _ = plot_objective(result, n_points=len(all_param)-num_of_solution_samples, minimum='expected_minimum')
    plt.savefig(save_data_folder)               # without white boxes savefig('foo.png', bbox_inches='tight')

start_time = time.time()

for Map_ID in range (0, No_of_maps):
    print("New map Id: " + str(Map_ID))
    if Activate_map_generator:
        save_data_folder = "../Optimization_data/Optimization_" + str(Map_ID)
    else:
        save_data_folder = "../Optimization_data/Single_map_Optimization_" + str(Map_ID)
    
    if not os.path.exists(save_data_folder):
        os.makedirs(save_data_folder)
    if not os.path.exists(save_data_folder + "/raw_simulation_data"):
        os.makedirs(save_data_folder + "/raw_simulation_data")

    """
    # Evaluate start robot possition: 
    while 1 == 1:
        r1x = int(random.randrange(1,len(grid_map[0])-1))
        r1y = int(random.randrange(1,len(grid_map[0])-1))
        r2x = int(random.randrange(1,len(grid_map[0])-1))
        r2y = int(random.randrange(1,len(grid_map[0])-1))
        if grid_map[r1y][r1x] < 0.5 and grid_map[r2y][r2x] < 0.5:   #No spawn point on obstacle
            break
    robot_pos = np.array([
                        [r1x,r1y],
                        [r2x,r2y],
                        ])
    """
    robot_start_pos = np.array([
                    [20,20],
                    [24,24],
                    ])
    #Handle the room
    if Activate_map_generator:
        grid_map = rg.room_generate(map_length, occupancy, max_size_obstacle,robot_start_pos)
    else:
        img = np.asarray(Image.open('../Maps/'+str(Map_ID)+'.pgm'))
        SIZE = len(img)
        grid_map = np.zeros((SIZE,SIZE))
        for row in range(0, SIZE):
            for column in range(0, SIZE):
                if img[row, column] < 100:
                    grid_map[row, column] = 0
                else:
                    grid_map[row, column] = 255
        #img.setflags(write=1)
        #grid_map = np.asarray(img)
        print (len(img))
        print (len(grid_map))
    save_as_pgm(save_data_folder + '/map '+ str(Map_ID)+'.pgm',grid_map)
    save_as_pgm('../mrs_packages/Simulation_Data/static_map.pgm',grid_map)

    # Generate the exploration task list
    exploration_tasks_text, Exploration_task_likelihood_image, Visualization = ets.generate_exploration_tasks(NO_OF_TASKS_U,NO_OF_TASKS_G,radius,obstacle_treshold,grid_map)
    save_as_txt(save_data_folder+"/exploration_tasks"+ str(Map_ID)+".txt",exploration_tasks_text)
    save_as_txt("../mrs_packages/Simulation_Data/exploration_tasks.txt",exploration_tasks_text)
    save_as_png(save_data_folder  + '/Exploration_task_liklehood'+ str(Map_ID)+'.png',Exploration_task_likelihood_image)
    #visualize(Visualization)

    for Task_ID in range (0,No_of_task_distr):
        
        #Generate the task list with the corresponding times, when the task is ampled
        tasks_txt, tasks_list = ts.generate_tasks(maximum_time,maximum_time_intervall,maximum_no_of_tasks,max_task_per_t,number_of_gauss_tasks_max, number_of_gauss_tasks_min, max_variance, number_of_uniform_tasks_max, number_of_uniform_tasks_min, grid_map,manual_tasks,max_equal_distriburion_number)
        save_as_txt(save_data_folder+"/tasks"+ str(Task_ID)+".txt",tasks_txt)
        save_as_txt("../mrs_packages/Simulation_Data/Tasks.txt",tasks_txt)
        #visualize(tasks_list)
        
        #Optimize the setup - Find the optimal hyperparameter
        Bayes, all_f_val, all_param, plot_f_val,result = opt.Bayes_optimize(Task_ID, num_of_solution_samples, num_of_parrallel_executed_solution_samples, Number_iter_next_sample, Bayes_iterations, Initial_random_samples,save_data_folder,Maximize)
        save_convergence_plot_data(save_data_folder+"/_ConvergencePlot_"+str(Task_ID)+".txt",plot_f_val,start_time)
        save_convergence_plot_figure(save_data_folder+"/_ConvergencePlot_figure_"+str(Task_ID)+".png",plot_f_val)
        try:
            save_objective_figure(save_data_folder+"/_objective_figure_"+str(Task_ID)+".png", result, all_param)
        except IndexError:
            print ("Error: Objective plot does not work")
            print (result.__sizeof__)
            print (len(all_param))
        save_Bayesian_raw_data(save_data_folder+"/_Bayes_raw_data_"+str(Task_ID)+".txt",result,all_f_val,all_param)
        #save_json(save_data_folder+"/_Sample_points_"+str(Map_ID)+".txt",result)