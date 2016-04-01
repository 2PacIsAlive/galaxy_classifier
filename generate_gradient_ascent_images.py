#!usr/bin/env python

from PIL  import Image
from glob import glob
from matplotlib.colors import rgb2hex
import json
import os

class Generator:
    def __init__(self):
        for file_ in glob('gradient_ascent_images/json/*'):
            img = Image.new( 'RGB', (64,64), "black")
            pixels = img.load()
            counter = 0
            with open(file_, 'r') as gradient_ascent_image:
                gradient_ascent_image = json.load(gradient_ascent_image)
                for i in range(img.size[0]):
                    for j in range(img.size[1]):
                        pixels[i,j] = self.getHexValue(gradient_ascent_image[counter])
                        counter += 1
            img.save('gradient_ascent_images/png/' + file_[28:-5]+'.png','png')
        for file_ in glob('layer_images/json/*'):
            img = Image.new( 'RGB', (5,5), "black")
            pixels = img.load()
            counter = 0
            with open(file_, 'r') as gradient_ascent_image:
                gradient_ascent_image = json.load(gradient_ascent_image)
                for i in range(img.size[0]):
                    for j in range(img.size[1]):
                        pixels[i,j] = self.getHexValue(gradient_ascent_image[counter])
                        counter += 1
            img.save('layer_images/png/' + file_[28:-5]+'.png','png')
        os.system('convert gradient_ascent_images/png/*.png animations/gradient_ascent_test.mpeg')
        os.system('convert layer_images/png/*.png           animations/hidden_unit_0.mpeg')
        os.system('open animations/gradient_ascent_test.mpeg')
        os.system('open animations/hidden_unit_0.mpeg')

    def getHexValue(self, value):
        v = str(int(value * 100000))
        while len(v) < 6:
            v += '0'
        return int(v[:2], 16), int(v[2:4], 16), int(v[4:6], 16)


