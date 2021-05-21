import matplotlib.pyplot as plt
import os
import ast
import numpy as np
import matplotlib as mpl

def generate_array(text):
    data_list = []

    text_array = text.split("\n")
    for line in text_array:
        line = line.lstrip('(')
        line = line.rstrip(')')
        line = line.split(",")
        #print(line)
        float_line = []
        for item in line:
            #print (item)
            try:
                float_line.append(float(item))
            except ValueError:
                print ("Value Error")
        data_list.append(float_line)
    data_list.pop()
    return data_list




#os.chdir(__file__[0:__file__.find('mrs_packages')+12])
# Read in the file
file = open("/home/don/catkin_ws/src/ma_julian_weick/code/mrs_packages/raw_data_output/simulator_output/candidate_11000.txt", "r")
text1 = file.read()
data_list1 = generate_array(text1)




#print (data_list)
plt.style.use('fivethirtyeight')
# GEnerate x and y
y1 = []


x1 = []

for item in data_list1:
    y1.append(item[2])
    x1.append(item[3])

# Include a line
ax.axhline(y=545.0305882352941, color='orange', ls='--',label='No policy')

# Add a text into the diagram
plt.text(0.31, 0.72,'Value', ha='center', va='center', transform=ax.transAxes)

# Add a arrow with discription
ax.annotate('Agents do not detected task sampling', xy=(5640, 720), xytext=(-11,-70), 
            textcoords='offset points', ha='center', va='bottom',
            bbox=dict(boxstyle='round,pad=0.2', fc='yellow', alpha=0.3),
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.2', 
                            color='red'))

#Linear regression:

xr = np.linspace(1300, 7200,num=len(param_list0))
X1 = np.array(x1[1300:])
A = np.vstack([X1, np.ones(len(X1))]).T
Y1 = np.array(y1[1300:])
m, c = np.linalg.lstsq(A, Y1, rcond=None)[0]

plt.plot(xr, m*xr + c, 'red', label='Task increase rate best first', ls='-.')

# Include colorbox:

plt.plot(xr, m*xr + c, 'red', label='Task increase rate best first', ls='-.')


mpl.style.use('default')
fig, ax = plt.subplots()
ax.grid(True)
print (len(y1))

ax.plot(x1, y1,label='First run')

ax.set_title("R1 path")
ax.set(xlabel='X coordinate', ylabel='Y coordinate')
#ax.set(xlabel='Iteration', ylabel='No. of tasks')
ax.legend()
plt.show()


