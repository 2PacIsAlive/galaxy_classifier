#usr/bin/env python

from galaxy_loader import Galaxies
from PIL import Image
import random
import pandas
import glob
import math
import sys
import os

class Neuron():
	def __init__(self):
		self.act = None
		self.inputConnections = []
		self.hiddenConnections = []
		self.outputConnections = []

class NeuralNetwork():
	def __init__(self):
		self.inputLayer = []
		self.hiddenLayer = []
		self.outputLayer = []
		self.epochError = 0
		self.epochs = 0

	def makeNetwork(self, input_size, hidden_size, output_size):
		for input_node in range(input_size):
			self.inputLayer.append(Neuron())
		for hidden_node in range(hidden_size):
			self.hiddenLayer.append(Neuron())
		for output_node in range(output_size):
			self.outputLayer.append(Neuron())

	def genInputActivations(self):
		for file_ in glob.glob("wavelets_medium/*"):
			Galaxy = Image.open(file_)
			pix = list(Galaxy.getdata())
			activation = []
			for pixel in pix:
				hexval = hex(pixel[0]) + hex(pixel[1])[:1] + hex(pixel[2])[:1]
				activation.append((int(hexval,16))/100000.0)
			self.inputActivations.append((activation,file_[16:-4]))

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
		#print "output:", f, "sigmoid:", self.sigmoid(f)
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
		#print layerActivity
		#print max(layerActivity, key = lambda x: x[1])
		return max(layerActivity, key = lambda x: x[1])

	def checkMinusPhaseOutput(self,Galaxy,minusPhaseOutput):
		#expected = self.getExpected(minusPhaseOutput[0],Galaxy)
		glxy = self.getGalaxy(minusPhaseOutput[0])
		#if minusPhaseOutput[0] == self.outputLayer[0]:
		#	glxy = "a_f"
		#elif minusPhaseOutput[0] == self.outputLayer[1]:
		#	glxy = "a_m"
		#print "Expected:", Galaxy[1], "Output:", glxy, "Node:", choice[0], "Activation:", choice[1]
		#print "a_f unit activation: ",self.outputLayer[0].act
		#print "a_m unit activation: ",self.outputLayer[1].act
		correct = False
		if Galaxy[1] == glxy:
			correct = True
		return correct, glxy

	def plusPhase(self,Galaxy,minusPhaseOutput):
		#for node, act in layerActivity:
			#print "node: ", node, "act: ", act
		#layerActivity.remove(choice)
		correct, glxy = self.checkMinusPhaseOutput(Galaxy,minusPhaseOutput)

		#BACKWARD
		outputCounter = 0
		for output in self.outputLayer:
			error = self.getExpected(output,Galaxy) - output.act
			hiddenCounter = 0
			for hidden in self.hiddenLayer:
				#the change in weights for each output/hidden connection are:
					#the error for the output node (expected - output) multiplied by the activation of the unit
				new_weight = (hidden.act * error) + output.hiddenConnections[hiddenCounter]
				#new_weight = (hidden.act * 0.05 * error) + output.hiddenConnections[hiddenCounter][1]
				#print output, correct, "old: ", output.hiddenConnections[hiddenCounter][1], "new: ",new_weight
				output.hiddenConnections[hiddenCounter] = new_weight
				hidden.outputConnections[outputCounter] = new_weight
				#error = self.getExpected(output,Galaxy) - hidden.act
				#print error, hidden.act, output.act
				inputCounter = 0
				for input_ in self.inputLayer:
					#the change in weights for each input node are:
						#the sum over all hidden units of:
							#the expected output multiplied by the weight for the hidden/input pair
						#minus the sum over all hidden units of:
							#the output unit's activation multiplied by the weight for the hidden/input pair
						#multiplied by yprime????
							#I think y prime is the activation of the hidden layer unit
					backprop_counter = 0
					tw = 0
					zw = 0
					for output_backprop in self.outputLayer:
						weight = output_backprop.hiddenConnections[hiddenCounter]
						tw += self.getExpected(output_backprop,Galaxy) * weight
						zw += output_backprop.act * weight
						backprop_counter += 1
					#new_weight = ((tw - zw) * hidden.act * input_.act) + hidden.inputConnections[inputCounter]
					new_weight = ((tw - zw) * (hidden.act * (1 - hidden.act) * input_.act)) + hidden.inputConnections[inputCounter]
					#print "EXPECTED:", self.getExpected(output,Galaxy), "ACTUAL:", output.act, "OLD:", hidden.inputConnections[inputCounter], "NEW:", new_weight
					#new_weight = (input_.act * 0.05 * error) + hidden.inputConnections[inputCounter][1]
					hidden.inputConnections[inputCounter] = new_weight
					input_.hiddenConnections[hiddenCounter] = new_weight
					inputCounter += 1
				hiddenCounter += 1
			outputCounter += 1
		if correct == False:
			return False
		else:
			return True

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
                print "Epoch:", self.epochs, "Error:", float(self.epochError) / float(len(galaxies.inputActivations))
                #print self.epochError
                '''
                if self.epochError > 1:
                    return self.train()
                else:
                    return
                '''

	def test(self):
		trial = 0
		for activation, Galaxy in galaxies.inputActivations:
			print "\nTrial: ", trial
			print "Galaxy: ", Galaxy[:-2]
			print "Gender: ", Galaxy[-1:]
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
	try:
		#net.test()
		print "beginning training...\n"
                for i in range(int(sys.argv[1])):
                    try:
                        net.train()
                    except KeyboardInterrupt:
                        break
		print "Success!"
		print "Error across 100 epochs: ", net.epochError
		print "Epochs to convergence:", net.epochs
        except Exception as e:
		print "training failed because of "+str(e)
	print "testing network...\n"
	net.test()
	#if raw_input("Would you like to save the network's weights? (y/n) ") == "y":
	#	net.saveWeights()
	net.saveWeights()
	print "weights saved\n"
	net.saveRFs()
        print "receptive fields saved\n"

if __name__=="__main__":
    galaxies = Galaxies()
    net = NeuralNetwork()
    main()
