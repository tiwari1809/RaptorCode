import math
# import numpy as np 
import random
# from scipy import *
from random import choices

#output to be stored at nodes	
codedBlocks=[]

	
##############PC MATRIX########################
#PC matrix is of dimension (N-k)x(N) in standard form it is stored as [P|I],
#Where P is of dimensions (N-k)x(k) and I is identity matrix of (N-k)x(N-k).
#We store positions of 1's in PC matrix.
#First entry of each row in PC matrix represents row number, 
#thereafter each number represesnts the block identity used, 
#the last one is fixed(different for each row) as it comes through I.
###############################################

#N-k = No. of parity eqautions.
#k = input symbols.
#d = check node's degree, which is constant.

def LDPCMatrix(N,k,d,PCMatrix):
	SumC=[0]*(k)
	SumR=[0]*(N-k)
	count1=0
	count2=0
	index=[i for i in range(0,k)]
	IstartCoeff=k #column number from where Idendity matrix starts
	for i in range (0,N-k):
		PCColumn=[i]
		for j in range (0, d-1):
			flag=1
			while(flag==1):
				a=random.choice(index)
				flag=0
				if(SumC[a]==2):
					index.remove(a)
					flag=1	
				# if(SumC[a]==1):
				# 	count1+=1
				# 	if(count1>((N-k)/5)*2):
				# 		# print("yes")
				# 		flag=1
				# # elif(SumC[a]<2):
				# 	count2+=1
				# 	if(count2>((N-k)/5)*3):
				# 		flag=1
			PCColumn+=[a]
			SumC[a]+=1
			SumR[i]+=1
		PCColumn+=[IstartCoeff]
		IstartCoeff+=1
		PCMatrix+=[PCColumn]
	# for i in range(0,len(SumR)):
	# 	print(SumR[i], end=" ")
	# for i in range(0,len(PCMatrix)):
	# 	print(PCMatrix[i])


def LTCodeDistribution(N):
	epsilon = 2.0/3.0 #for k=10,000 input symbols
	mhu= (2.0*epsilon + epsilon*epsilon)/4.0 # mhu = eps/2 + (eps/2)^2
	D=9.0 #max-degree=upperBound((4*(1+eps))/eps) 

	#defining coefficients of x^i
	probabilities = [0.0, mhu/(mhu+1)]
	probabilities += [1.0/((mhu+1)*((i)*(i-1))) for i in range (2,int(D)+1)]
	probabilities+=[1.0/((mhu+1)*D)]
	probabilities += [0.0 for i in range (int(D)+2,int(N))]
	su=0.0
	for i in range(0,len(probabilities)):
		if(i<=12):
			# probabilities[i]='{:<020}'.format(probabilities[i])
			# print(probabilities[i])
			su+=(probabilities[i])
		else:
			break
	# print ("prob",probabilities)
	print(su)
	return probabilities

#returns the value d for a block i.e degree for any block
def getDegrees(N,c):
	probabilities= LTCodeDistribution(N)

	blocks = [i for i in range(0,int(N))]
	#c=droplet quantity
	#N=k+p
	return choices(blocks, weights=probabilities, k=int(c))


class codedBlockStruct: 
	def __init__(self, degree, neighbours, flag): #header might be needed in future
		self.degree=degree
		self.neighbours=neighbours
		self.flag=0 #checks maliciousness of a block
		# self.data=data

#returns indexes for a given block provided degree=d
def getIndex(deg,blocksN):
	# random.seed(deg)
	indexes= random.choices(range(blocksN), k=deg)
	return indexes

def encoder():
	N=12500.0
	c=10.0 #for starge saving = 500
	
	#######LDPC Encoder.
	PCMatrix=[]
	LDPCMatrix(12500, 10000, 8,PCMatrix)
	IntermediateBlocks=[]
	for i in range (0,len(PCMatrix)):
		IntermediateBlocks+=[PCMatrix[i]]

	print(IntermediateBlocks)

	#########LT Encoder
	
	#Each index i here represents index from intermediate blocks + k original blocks
	deg = getDegrees(N,c)
	# print ("deg",deg, "length", len(deg)) 
	for i in range(int(c)):
		indexes=getIndex(deg[i],12500)
		# print ("index",indexes)
		codedBlock=codedBlockStruct(deg[i],indexes,0)
		# codedBlock.data=blocks[indexes[0]]
		# for j in range(1,deg):
		# 	codedBlock.data= codedBlock.data^blocks[j]

		# codedBlocks += codedBlock

	return codedBlocks
encoder()

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
# decoder(codedBlocks,12500,9)