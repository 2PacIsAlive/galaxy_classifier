#!usr/bin/env python

import glob
import numpy
import pylab
import pandas
from PIL import Image

class Galaxies:

    inputActivations = []

    def __init__(self):
        self.data_matrix = self.loadTrainingData()

    def loadTrainingData(self):
        print "\nloading training data..."
        classifications = pandas.read_csv('solutions.csv')
        # currently only trying to discern whether the galaxy is:
            # 1.1) smooth
            # 1.2) having features/disk
            # 1.3) star/artifact
        classifications.drop(classifications.columns[4:38], axis=1, inplace=True) # get rid of all other classifications
        for file_ in glob.glob("training_images/*"):
            print file_, "loaded"
            galaxy     = Image.open(file_)
            pix        = list(galaxy.getdata())
            activation = []
            # color based
            for pixel in pix:
                hexval = hex(pixel[0]) + hex(pixel[1])[:1] + hex(pixel[2])[:1]
                activation.append((int(hexval,16))/100000.0)
            # edge detector
            '''
            img = Image.open(open('doc/images/3wolfmoon.jpg'))
            # dimensions are (height, width, channel)
            img = numpy.asarray(img, dtype='float64') / 256.

            # put image in 4D tensor of shape (1, 3, height, width)
            img_ = img.transpose(2, 0, 1).reshape(1, 3, 639, 516)
            filtered_img = f(img_)

            # plot original image and first and second components of output
            pylab.subplot(1, 3, 1); pylab.axis('off'); pylab.imshow(img)
            pylab.gray();
            # recall that the convOp output (filtered image) is actually a "minibatch",
            # of size 1 here, so we take index 0 in the first dimension:
            pylab.subplot(1, 3, 2); pylab.axis('off'); pylab.imshow(filtered_img[0, 0, :, :])
            pylab.subplot(1, 3, 3); pylab.axis('off'); pylab.imshow(filtered_img[0, 1, :, :])
            pylab.show()
            '''
            galaxy_id = int(file_[16:-4])
            df_row    = classifications[classifications.GalaxyID == galaxy_id]
            smooth    = df_row["Class1.1"] # probability that the galaxy is smooth
            feat_disk = df_row["Class1.2"] # probability that the galaxy has features/disk
            star      = df_row["Class1.3"] # probability that the image is a star or artifact
            if max([float(smooth), float(feat_disk), float(star)]) == float(smooth): # currently trying to detect smooth galaxies
                self.inputActivations.append((activation, 'smooth'))
            else:
                self.inputActivations.append((activation, 'not_smooth'))
