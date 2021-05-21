"""
script to clean grey pixels from pgm file
"""
import numpy as np
from netpbmfile import imwrite
import matplotlib.image as mpimg

# import gridmap
img = mpimg.imread('static_map.pgm') 

data = np.asarray(img)
SIZE = int(data.shape[0])

# read map layout

grid_map = np.zeros((SIZE,SIZE))
for row in range(0, SIZE):
    for column in range(0, SIZE):
        pixel = data[row][column]
        if pixel <= 100:
            grid_map[row, column] = 0
        else:
            grid_map[row, column] = 255


#grid_map[np.where(grid_map>-0.5)] = 1

imwrite('static_map_clean.pgm', grid_map.astype(int))

