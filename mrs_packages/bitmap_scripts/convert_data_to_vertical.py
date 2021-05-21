"""
a script to change the format of text files from horizontol to vertical
ie. take space-separated values and make them line-separated
"""
dirs= ['/home/defaultuser/Desktop/Probability_exploration', 
    '/home/defaultuser/Desktop/Probability_chosing_task', 
    '/home/defaultuser/Desktop/overall/Real_deal_1', 
    '/home/defaultuser/Desktop/overall/Real_deal_2', 
    '/home/defaultuser/Desktop/overall/Real_deal_collaborative_GBF_1', 
    '/home/defaultuser/Desktop/overall/test1', 
    '/home/defaultuser/Desktop/Cluster_only_GBF', 
    '/home/defaultuser/Desktop/Cluster_with_GBF_and_Cluster', 
    '/home/defaultuser/Desktop/Cluster_with_GBF_and_Cluster_and_Entropy', 
    '/home/defaultuser/Desktop/GBF_without_Exploration', 
    '/home/defaultuser/Desktop/GBF_with_Exploration', 
    
    ]
names = ['/x_data', '/y_data']

for direc in dirs:
    for name in names:
        filename = direc + name
        f_in = open(filename + '.txt', "r")
        data = f_in.readline()
        data = data.split(' ')

        f_out = open(filename + '_vertical.txt', "w")
        text = ''
        for d in data:
            text += str(d)
            text += '\n'

        f_out.write(text)
        f_out.close()
        f_in.close()
