# CPS Adaption Evaluation and Development Framework
for questions: julian.weick@tum.de  
Have Fun!


## Table of contents
* [General info](#general-info)
* [Screenshots](#screenshots)
* [Technologies](#technologies)
* [Setup](#setup)
* [Features](#features)
* [Status](#status)
* [Inspiration](#inspiration)
* [Contact](#contact)

### Evaluation
Contains the output images and data we used to evaluate our system.
### bitmap_scripts
Contains several Python scripts we used to generate our test cases. Also contains text and image files for these test cases.
### bitmap_visualiser
Contains the source code for the `bitmap_visualiser_node`. This node is responsible for saving image files, ie 'bitmaps', to visualize our contribution during the simulation. This folder also contains a Python script to combine the saved images into a gif.
### goal_communicator
Contains the source code for the `goal_communicator`. This node receives the next goal from `policy_node` and provides it to the `move_base`.
### map_handler
Contains the source code for the `map_handler_node`. This node keeps track of:
*  robot locations
*  discovered and not yet cleaned dirt locations
*  inferred probability distribution of new dirt appaerance
*  which regions of the map have not been observed in a long time

### policy 
Contains the source code for the `policy_node`. This node determines which robot should pursue which task next, by assigning a priority to each task. There are five components used while determining this priority value:
1.  Greedy-Best-First  
Closer tasks have higher priority.
2.  Clustering  
We cluster the dirt using k-means. Tasks that belong to larger clusters have higher priority.
3.  Neighborhood  
A task has higher priority if there is high probability of new tasks appearing in its neighborhood.
4.  Explore  
A task has higher priority if it is in an area that has not been observed in a long time.
5.  Entropy  
A task that is far from robot 1 is more interesting to robot 2 than dirt that is
at the same distance to robot 2, but closer to robot 1. This importance value is
then multiplied with the entropy of the distribution of dirt on the map.
The overall priority is a weighted sum of these tasks. The optimization of this weights is performed using the scripts in `Simualtion and Optimization scripts`.
### task_handler
Contains the source code for the `task_handler_node`. If there are conflicting reading obtained by the two robots, this node resolves the conflict. Then it notifies the `map_handler_node` of the newly discovered task.
### task_simulator
Contains the source code for the `task_simulator_node`.  This node simulates the sensors on the robots. It distributes new tasks on the map, which it gets from a .txt file. The format of the tasks in the txt file is (x_coordinate, y-coordinate, spawn time). 
The spawn of the tasks is related to the number how often the task simulator has been called by the map handler (in our case called means the task simulator gets a topic update on the topic robot location simulation). 
The idea is that the map handler will give the update tact for the whole system and the task simulator is supposed to work like a sensor, which gives the information as soon as it gets called.

### simulator
Contains the source code for the `simulator_node`. It replaces Gazebo with the benefit of a deterministic AMCL ( Adaptive Monte Carlo Localization) and move_base (path planing algorithm). Therefore the map is discretized, and the localization is simulated as the known exact position plus (random) offset and (gaussian) noise. For path planing a A* star planer has been implemented. For performance reasons the implementation language is cython and the code can be found in the folder astar_cython. Note that a A* algorithm in plain python3 is available (a_star_ad.py). Further note, that the move base has been designed to (more or less plug and play :) ) change the planing algorithms to the alorithms programmed in the PythonRobotics project by AtsushiSakai (https://github.com/AtsushiSakai/PythonRobotics) (Owesome project with a lot of modules worth implementing in the framework, MIT license).
 
### Watchdog
Contains the source code for the `watchdog_node`. If the simulation system is stuck, the watchdog send a signal to start the Trigger chain (explained in a section below) again. Got obsolete with a watchdog implementation in the Opt.py

## Simulation and Optimization scripts

Several scripts supporting the optimization of the weigts of the policy modules have been implemented:

### Opt.py
The Optimizer script, using Bayesian optimization. The Optimzer calls multiple samples (black box functions returning only a fitnes value) simultaniously for performance increase. Keeps track of the runing samples and is able or reset them if they get stuck.

### Communicate.py
Interface wraper starts the different sample.py under different domain names. This enables the system to parralelize the simulations, since every simulation needs to run on its own ROS core. 

### sample.py
Initializes the corresponding ROS nodes and sets the ROS parameter server.

### GA.py
Untested Implementation of a Genetic algorithm approach. Got obsolete because we are using a Bayesian optimizer in the approach.

### parameter_handler.py
Initializes the parameter for the simulation according to different patterns (static, random).

### parameter_space_exploration.py
Initializes the parameter for the simulation according to explore the parameter space systematicaly.

## Parameters
### bitmap_visualiser
*  `VISUALIZE_FREQUENCY`: Frequency (in seconds) to create and save the bitmap to visualise the state of the system.
### map_handler
*  `SIZE`: Size of the map (map is assumed to be square).
*  `PUBLISH_FREQUENCY`: Frequency (in seconds) to publish grid maps and task list, and to upcount the exploration of the cells.
*  `broom_size`: How close the robot should be to a dirt to clean it.
*  `prob_effect_radius`: When dirt appears in a location, this increases the probability of dirt appearing in a circular area surrounding it. This is the radius of that area.
*  `radius`: Detection radius, for both robots.
*  `ALPHA`: Weight of old probabilities in relation to newly appearing task.

### task_handler
*  `equaltaskthreshold`:  Distance threshold below two tasks are merged to one by averaging the position

### task_simulator
*  `detectionradius`: Is fetched from the taskhandler via the topic robotlocationsimulation, which fetchesit from the maphandler node via the topic robotlocation topic.
*  `wallhack`:  If it is true the robot can detect dirt true walls, but it can not clean true walls
*  `FNrate`:  Probability, that dirt will not be detected, even if it is in detection range.
*  `FPrate`:  Probability, that dirt will be detected even if there is no dirt.
*  `sensornoisesigmax`:  Sigma of a Gaussian distribution for the simulation of the position noise of thesensor in x direction
*  `sensornoisesigmay`:  Sigma of a Gaussian distribution for the simulation of the position noise of thesensor in y direction
*  `sensortolerance`: If True the sensor will have the tolerance Sigma specified.  If False the sensor is perfectin terms of noise

### policy_node
* `NUM_CLUSTERS`: number of total clusters
* `NORM_CLUSTER`: relative importance of the clustering in the policy
* `SURROUND_RAD`:  how many cells in the neighborhood are considered
* `NORM_SURROUND`: weight of the probability value approach
* `NORM_SURROUND_EXPLORATION`: effect of the probability for the choice of exploration tasks
* `NORM_ENTROPY`: weight of the entropy repulsion
* `NORM_EXPLORATION`: weight of the exploration counter
* `EXPLORATION_DISTANCE_BONUS`: incentive to choose the second exploration task far away from the first one
* `COLLABORATION`: if set to False, one task can be assigned to both robots
* `IGNORANT_EXPLORATION`: if set to True, the exploration tasks are not chosen according to their upcounting and probability values, but randomly

### Opt

* `num_of_solution_samples`: Determins the total amount of samples per iteration of the Bayesian optimization approach
* `num_of_parrallel_executed_solution_samples`: Determins how many samples are executed in parrallel on the machine
* `Number_iter_next_sample`: Determins how many iterations are performed in the simulation
* `Diverse UB and LB`: Upper and lower bound of the hyperparameter respectifely
* `Optimizer parameter`: Several parameter of the Optimization approach see https://scikit-optimize.github.io/stable/modules/classes.html for more.
* `Bayes_iterations`: How many iterations on the Bayesian optimizer.


