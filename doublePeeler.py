import math
import numpy as np 
import random
from scipy import *
from random import choices

def raptorDistribution(N):
	epsilon = 2.0/3.0 #for N=10k imput symbols

	mhu= (2.0*epsilon + epsilon*epsilon)/4.0 # mhu = eps/2 + (eps/2)^2

	D=10 #max-degree=upperBound((4*(1+eps))/eps) 


	#defining coefficients of x^i
	probabilities = [0, mhu/(mhu+1)]
	probabilities += [1.0/((i)*(i-1)) for i in range (2,D)]
	probabilities+=[1.0/D]
	probabilities += [0 for i in range (D,N-1)]

	return probabilities


def getDegrees(N,c):
	probabilities= raptorDistribution(N)

	blocks = [i for i in range(N)]
	#c=droplet quantity
	#N=k+p
	return choices(blocks, weights=probabilities, k=c)

class codedBlockStruct: 
	def __init__(self, degree, neighbours, flag,data): #header might be needed in future
		self.degree=degree
		self.neighbours=neighbours
		self.flag=0
		self.data=data
		
def getIndex(deg,blocksN):
	random.seed(deg)
	indexes= random.choices(range(blocksN), k=deg)
	return indexes

def encoder(blocks):
	deg = getDegrees(N,c)
	codedBlocks=[]
	for i in range(c):
		indexes=getIndex(deg)
		codedBlock.degree=deg
		codedBlock.neighbours=indexes
		codedBlock.data=blocks[indexes[0]]
		for j in range(1,deg):
			codedBlock.data= codedBlock.data^blocks[j]

		codedBlocks += codedBlock

	return codedBlocks
def removeDegree(block, codedBlocks):
	for codedBlock in codedBlocks:
		for neighbour in codedBlock.neighbours:
			if (block==neighbour):
				codedBlock=codedBlock^block
				codedBlock.degree-=1

def decoder(codedBlocks,N,D):
	recoveredBlocks=0
	downloadedBlocks=D
	originalBlocks=[]
	while recoveredBlocks<N or downloadedBlocks>0:
		for codedBlock in codedBlocks:

			if(codedBlock.degree==1):
				downloadedBlocks-=1
				if(codedBlock.header == header):  #To DO retrieve headers
					recoveredBlocks+=1
					originalBlocks+=codedBlock
					removeDegree(codedBlock, codedBlocks)
				else:
					#to make it marks as a malicious nodes
					codedBlock.flag=1
