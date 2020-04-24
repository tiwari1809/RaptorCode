import math
# import numpy as np 
import random
# from scipy import *
from random import choices
import csv

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
	IstartCoeff=k+1 #column number from where Idendity matrix starts
	for i in range (0,N-k):
		PCColumn=[i+1+10000] #assigning index to each intermediate level coded block
		for j in range (0, d-1):
			flag=1
			while(flag==1):
				a=random.choice(index)
				flag=0
				if(SumC[a]==2):
					index.remove(a)
					flag=1	
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
			su+=(probabilities[i])
		else:
			break
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

def encoder(NodeNo):
	N=12500.0
	c=10.0 #for starge saving = 500
	
	#############  LDPC Encoder  ################
	PCMatrix=[]
	LDPCMatrix(12500, 10000, 8, PCMatrix)
	IntermediateBlocks=[]
	for i in range (0,len(PCMatrix)):
		IntermediateBlocks+=[PCMatrix[i]]
	# print(IntermediateBlocks)
	with open("Final Encoded Blocks.csv", "w+") as f:
		f.write("Node Number"+ "," + str(NodeNo))
		f.write("\n")
		f.write("," + "IntermediateBlocks" + " " + str(NodeNo))#Nodeno, for decoding purpose
		f.write("\n")
		for i in range(0,len(IntermediateBlocks)):
			f.write(",")
			for j in range(0,len(IntermediateBlocks[i])):
				f.write("," + str(IntermediateBlocks[i][j]))
			f.write("\n")

		
		############## LT Encoder  ################
		
		#writing of coded blocks in file
		f.write("," + "Coded Blocks" + " " + str(NodeNo))#Nodeno, for decoding purpose
		f.write("\n")		

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

			#i writes the index of coded block
			f.write("," + "," + str(i+1))
			for i in range(0, len(codedBlock.neighbours)):
				f.write("," + str(codedBlock.neighbours[i]))
			f.write("\n")
	f.close()
# print(codedBlocks)	

############## Call Encoder Function ##################
# T=1
# while(T):
# 	print(T)
# 	encoder(T)
# 	T-=1




########### Decoding ##############
def downloadBlocks(T):
	NodeNo=T
	DownloadedBlocksNo=16667 # k(1+epsilon) to be downloaded
	DownloadedBlockNodeIndexes = random.choices(range(1,NodeNo),k=DownloadedBlocksNo)
	# print(DownloadedBlockNodeIndexes)
	return(DownloadedBlockNodeIndexes)
# downloadBlocks(2002)

def removeDegree(block, codedBlocks):
	for codedBlock in codedBlocks:
		for neighbour in codedBlock.neighbours:
			if (block==neighbour):
				codedBlock=codedBlock^block
				codedBlock.degree-=1

def decoder(N,D):
	recoveredBlocks=0
	downloadedBlocks=D
	originalBlocks=[]
	IntermediateBlocks=[]
	codedBlocks=[]
	DownloadedBlockNodeIndexes=downloadBlocks(2002)
	with open("Final Encoded Blocks.csv", "r") as f:
		reader = csv.reader(f)
		flag=0
		for row in reader:
			if(flag==0):
				for i in range(0,len(row)):
					if("Node Number" in row[i]):
						i+=1
						for index in DownloadedBlockNodeIndexes:
							if(str(index)==str(row[i])):
								flag=1
			if(flag==1):
				T=2500
				row=next(reader)
				while(T):
					row=next(reader)					
					IntermediateBlocks+=[row[3:]]
					T-=1
				T=10
				row=next(reader)
				while(T):
					row=next(reader)
					codedBlocks+=[row[3:]]
					T-=1
				recoveredBlocks=LTDecoder(codedBlocks)
				flag=0
	

def LTDecoder(codedBlocks):
	recoveredBlocks=[]
	recoveredBlock=None
	flag=0
	# print((codedBlocks))
	while(len(codedBlocks)>1):
		if(flag==1):
			break
		flag=0
		for blocks in codedBlocks:
			print(blocks, len(blocks))
			if(len(blocks)==1):
				flag=2
				for block in blocks:
					recoveredBlock=blocks
				recoveredBlocks+=[recoveredBlock]
				codedBlocks.remove(blocks)
				# XORing the block recovered to make more degree 2 blocks
				for blocks in codedBlocks:
					for block in blocks:
						if(recoveredBlock in blocks):
							blocks.remove(recoveredBlock)
		if(flag==0):	
			# print("Unable to decode all Coded blocks")
			flag=1
			# print(recoveredBlocks)
			break
		# print(len(codedBlocks))
	return recoveredBlocks
	# while recoveredBlocks<N or downloadedBlocks>0:
	# 	for codedBlock in codedBlocks:

	# 		if(codedBlock.degree==1):
	# 			downloadedBlocks-=1
	# 			if(codedBlock.header == header):  #To DO retrieve headers
	# 				recoveredBlocks+=1
	# 				originalBlocks+=codedBlock
	# 				removeDegree(codedBlock, codedBlocks)
	# 			else:
	# 				#to make it marks as a malicious nodes
	# 				codedBlock.flag=1
decoder(12500,9)