#usr/bin/env python

from firebase.firebase import FirebaseApplication, FirebaseAuthentication
from generate_gradient_ascent_images import Generator
from galaxy_loader import Galaxies
from PIL import Image
import random
import pandas
import glob
import math
import json
import sys
import os

class Neuron():
	def __init__(self):
		self.act = None
		self.inputConnections  = []
		self.hiddenConnections = []
		self.outputConnections = []

class NeuralNetwork():

        authentication = FirebaseAuthentication('zSLMGZaEXRrxLB7kvYP86ZXavdVPiNR55QTJnt4O', 'jared.jolton@gmail.com', True, True)
        firebase       = FirebaseApplication('https://galaxy-classifier.firebaseio.com', authentication)

	def __init__(self):
                self.genImgs = False
                if sys.argv[2] == '1':
                    self.genImgs  = True
		self.alpha    = float(sys.argv[3])
		self.interval = int(sys.argv[4])
		self.newPixels   = dict()
                self.inputLayer  = []
		self.hiddenLayer = []
                self.outputLayer = []
		self.epochError  = 0
		self.epochs      = 18076

	def makeNetwork(self, input_size, hidden_size, output_size):
		for input_node in range(input_size):
			self.inputLayer.append(Neuron())
		for hidden_node in range(hidden_size):
			self.hiddenLayer.append(Neuron())
		for output_node in range(output_size):
			self.outputLayer.append(Neuron())

	def sigmoid(self,activation):
		try:
			return 1 / (1 + math.exp(-activation))
		except OverflowError:
			return 0

	def hiddenActivationFunction(self,node,index):
		xw = 0
		#zw = 0
		for input_node in self.inputLayer:
			xw += input_node.hiddenConnections[index] * float(input_node.act)
		#for output_node in self.outputLayer:
		#	zw += output_node.hiddenConnections[index] * float(input_node.act)
		#return self.sigmoid(xw + zw)
		return self.sigmoid(xw)

	def outputActivationFunction(self,node,index):
		f = 0
		for hidden_node in self.hiddenLayer:
			f += hidden_node.outputConnections[index] * float(hidden_node.act)
		return self.sigmoid(f)

	def getGalaxy(self,node):
		if node == self.outputLayer[0]:
			return "smooth"
		elif node == self.outputLayer[1]:
			return "not_smooth"

	def getExpected(self,node,Galaxy):
		if Galaxy[1] == "smooth":
			if node == self.outputLayer[0]:
				return 1
			else:
				return 0
		elif Galaxy[1] == "not_smooth":
			if node == self.outputLayer[1]:
				return 1
			else:
				return 0

	def trainingEpoch(self):
		file_ = 0
		for Galaxy in galaxies.inputActivations:
			output = self.minusPhase(Galaxy)
			if self.plusPhase(Galaxy,output) == False:
				self.epochError += 1
                if self.genImgs:
                    if self.epochs % self.interval == 0:
    			self.saveNewPixels()

	def minusPhase(self,Galaxy):
		#FORWARD
		input_counter = 0
		for input_node in self.inputLayer:
			input_node.act = Galaxy[0][input_counter]
			input_counter += 1
		hiddenConnection = 0
		for hidden in self.hiddenLayer:
			hidden.act = self.hiddenActivationFunction(hidden,hiddenConnection)
			hiddenConnection += 1
		outputConnection = 0
		layerActivity = []
		for output in self.outputLayer:
			output.act = self.outputActivationFunction(output,outputConnection)
			layerActivity.append((output,output.act))
			outputConnection += 1
		return max(layerActivity, key = lambda x: x[1])

	def checkMinusPhaseOutput(self,Galaxy,minusPhaseOutput):
		glxy = self.getGalaxy(minusPhaseOutput[0])
		correct = False
		if Galaxy[1] == glxy:
			correct = True
		return correct, glxy

	def plusPhase(self,Galaxy,minusPhaseOutput):
		correct, glxy = self.checkMinusPhaseOutput(Galaxy,minusPhaseOutput)

		#BACKWARD
		outputCounter = 0
		for output in self.outputLayer:
			error = self.getExpected(output,Galaxy) - output.act
			hiddenCounter = 0
			for hidden in self.hiddenLayer:
				new_weight = (hidden.act * error) + output.hiddenConnections[hiddenCounter]
				output.hiddenConnections[hiddenCounter] = new_weight
				hidden.outputConnections[outputCounter] = new_weight
				inputCounter = 0
				for input_ in self.inputLayer:
					backprop_counter = 0
					tw = 0
					zw = 0
					for output_backprop in self.outputLayer:
						weight = output_backprop.hiddenConnections[hiddenCounter]
						tw += self.getExpected(output_backprop,Galaxy) * weight
						zw += output_backprop.act * weight
						backprop_counter += 1
					new_weight = ((tw - zw) * (hidden.act * (1 - hidden.act) * input_.act)) + hidden.inputConnections[inputCounter]
					#print "EXPECTED:", self.getExpected(output,Galaxy), "ACTUAL:", output.act, "OLD:", hidden.inputConnections[inputCounter], "NEW:", new_weight
					hidden.inputConnections[inputCounter] = new_weight
					input_.hiddenConnections[hiddenCounter] = new_weight
					self.updatePixel(Galaxy, inputCounter, (new_weight * self.alpha))
					inputCounter += 1
				hiddenCounter += 1
			outputCounter += 1
		if correct == False:
			return False
		else:
			return True

	def updatePixel(self, Galaxy, inputCounter, new_weight):
	    self.newPixels[Galaxy[1]][inputCounter] = self.newPixels[Galaxy[1]][inputCounter] + new_weight

	def initializeRandomWeights(self):
		for input_node in self.inputLayer:
			for hidden_node in self.hiddenLayer:
				randomWeight = random.uniform(-1,1)
				#input_node.hiddenConnections.append((hidden_node,randomWeight))
				input_node.hiddenConnections.append(randomWeight)
				#hidden_node.inputConnections.append((input_node,randomWeight))
				hidden_node.inputConnections.append(randomWeight)
		for hidden_node in self.hiddenLayer:
			for output_node in self.outputLayer:
				randomWeight = random.uniform(-1,1)
				#hidden_node.outputConnections.append((output_node,randomWeight))
				hidden_node.outputConnections.append(randomWeight)
				#output_node.hiddenConnections.append((hidden_node,randomWeight))
				output_node.hiddenConnections.append(randomWeight)

	def loadWeights(self):
		file_ = raw_input("Enter name of weights file: ")
		file_ = open(file_+".data","r")
		weights = []
		for weight in file_:
			weights.append(float(weight))
		file_.close()
		for input_node in self.inputLayer:
			for hidden_node in self.hiddenLayer:
				#input_node.hiddenConnections.append((hidden_node,weights[0]))
				input_node.hiddenConnections.append(weights[0])
				#hidden_node.inputConnections.append((input_node,weights[0]))
				hidden_node.inputConnections.append(weights[0])
				weights.pop(0)
		for hidden_node in self.hiddenLayer:
			for output_node in self.outputLayer:
				#hidden_node.outputConnections.append((output_node,weights[0]))
				hidden_node.outputConnections.append(weights[0])
				#output_node.hiddenConnections.append((hidden_node,weights[0]))
				output_node.hiddenConnections.append(weights[0])
				weights.pop(0)

	def train(self):
                self.epochError = 0
                self.trainingEpoch()
                self.epochs += 1
                error = float(self.epochError) / float(len(galaxies.inputActivations))
                print "Epoch:", self.epochs, "Error:", error
                if self.epochs % 25 == 0:
                    self.firebase.post('/error', {'epoch': self.epochs, 'err': error})

	def test(self):
		trial = 0
		for activation, Galaxy in galaxies.inputActivations:
			print "\nTrial: ", trial
			print "Galaxy: ", Galaxy
			output = self.minusPhase((activation,Galaxy))
			correct, glxy = self.checkMinusPhaseOutput((activation,Galaxy),output)
			if correct == True:
				print "Correct!", "Output: ", glxy
			else:
				print "Test failed.", "Output: ", glxy
			trial += 1

	def saveWeights(self):
                weights = open(raw_input("Enter name for data: ")+".data","w")
		for node in self.inputLayer:
			for connection in node.hiddenConnections:
				weights.write(str(connection))
				weights.write("\n")
		for node in self.hiddenLayer:
			for connection in node.outputConnections:
				weights.write(str(connection))
				weights.write("\n")
		weights.close()

	def saveRFs(self):
    		rf_counter = 0
		for hidden in self.hiddenLayer:
			rf = open("hidden_unit_receptive_fields/"+str(rf_counter)+".data","w")
			for weight in hidden.inputConnections:
				rf.write(str(weight))
				rf.write("\n")
			rf.close()
			rf_counter += 1
        	rf_counter = 0
		for output in self.outputLayer:
			rf = open("output_unit_receptive_fields/"+str(rf_counter)+".data","w")
			for weight in output.hiddenConnections:
				rf.write(str(weight))
				rf.write("\n")
			rf.close()
			rf_counter += 1

	def setupGradientAscent(self):
		self.newPixels = {  
                                    'smooth':     random.choice([example[0] for example in galaxies.inputActivations if example[1] == 'smooth']),    # pick a random smooth galaxy image to start
				    'not_smooth': random.choice([example[0] for example in galaxies.inputActivations if example[1] == 'not_smooth']) # pick a random not_smooth galaxy image to start
		    		 }

	def saveNewPixels(self):
		with open('gradient_ascent_images/json/smooth_new_pixels_' + str(self.epochs)     + '.json', 'w') as new_smooth:
			json.dump(self.newPixels['smooth'], new_smooth)
		with open('gradient_ascent_images/json/not_smooth_new_pixels_' + str(self.epochs) + '.json', 'w') as new_not_smooth:
			json.dump(self.newPixels['not_smooth'], new_not_smooth)
	    	with open('layer_images/json/hidden_weights_' + str(self.epochs) + '.json', 'w') as hidden_weights_file:
			json.dump(self.inputLayer[0].hiddenConnections, hidden_weights_file)
	
                print 'images saved for epoch ' + str(self.epochs)

def main():
	net.makeNetwork(
                        len(galaxies.inputActivations[0]), # input size
                        50,                                # hidden size
                        2								   # output size
                       )
	if raw_input("Would you like to load weights? (y/n) ") == "y":
		print "loading weights...\n"
		net.loadWeights()
	else:
		print "initializing random weights...\n"
		net.initializeRandomWeights()
	net.setupGradientAscent()
        print "beginning training...\n"
	for i in range(int(sys.argv[1])):
		try:
			net.train()
		except KeyboardInterrupt:
			break
	print "Success!"
	print "Error across 100 epochs: ", net.epochError
	print "Epochs to convergence:", net.epochs
	print "testing network...\n"
	net.test()
	net.saveWeights()
	print "weights saved\n"
	net.saveRFs()
        print "receptive fields saved\n"
        print "generating images..."
        if net.genImgs:
            Generator()

if __name__=="__main__":
    galaxies = Galaxies()
    net = NeuralNetwork()
    main()
