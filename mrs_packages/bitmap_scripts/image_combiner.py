"""
script to combine several runs' bitmap images together for visulaization purposes
"""
import sys
from PIL import Image


for i in range(1, 2140):
    name1 = '/home/defaultuser/Desktop/Real_deal_8_1/' + str(i) + '_step.png'
    image1 = Image.open(name1)

    name2 = '/home/defaultuser/Desktop/Real_deal_GBF_1/' + str(i) + '_step.png'
    image2 = Image.open(name2)

    new_im = Image.new('RGB', (700,460))
    new_im.paste(image1,(20,20))
    new_im.paste(image2,(20,240))
    name = '/home/defaultuser/Desktop/combined/' + str(i) + '_step.png'
    new_im.save(name)
