"""
a script to add black areas over generated bitmap images for animation purposes
"""
import sys
from PIL import Image
import numpy as np

for i in range(1, 2140):
    name = '/home/defaultuser/Desktop/combined/' + str(i) + '_step.png'
    image1 = Image.open(name)

    new_im = Image.new('RGB', (700,460))

    data = np.zeros((430, 430, 3))
    black = Image.fromarray(data, 'RGB')

    new_im.paste(image1,(0,0))
    new_im.paste(black,(250,240))
    name = '/home/defaultuser/Desktop/combined2/' + str(i) + '_step.png'
    new_im.save(name)
