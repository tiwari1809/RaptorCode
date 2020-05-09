import math
import random
from random import choices
import csv
import numpy as np

"""
##############PC MATRIX########################
PC matrix is of dimension (N-k)x(N) in standard form it is stored as [P|I],
Where P is of dimensions (N-k)x(k) and I is identity matrix of (N-k)x(N-k).
We store positions of 1's in PC matrix.
First entry of each row in PC matrix represents row number, 
thereafter each number represesnts the block identity used, 
the last one is fixed(different for each row) as it comes through Identity matrix.

#N-k = No. of parity equations.
#k = input symbols.
#d = check node's degree, which is constant.

"""

def mod(a):
	if(a>0):
		return a
	else:
		return -a

def LDPCParityMatrixGenerator(N,k,d):
	SumC=[0]*(N+1)
	SumR=[0]*(N-k)
	countR=0
	countC=0
	temp=[]
	PCMatrix=[]
	index=[i for i in range(1,N+1)]
	colWith2=[]
	for i in range (0,N-k):
		countR=0
		PCRow=[]
		prevA=N+5	
		for j in range (0, d):
			flag=1
			while(flag==1):
				col=random.choice(index)
				flag=0
				if(SumC[col]==2):
					colWith2+=[col]
					index.remove(col)
					flag=1	
				if(col in temp): #to check number of 1's common between two rows
					countR+=1
					if(countR>1):
						flag=1
			PCRow+=[col]
			prevA=col
			SumC[col]+=1
			SumR[i]+=1
		temp=[]
		temp+=[PCRow]
		PCMatrix+=[PCRow]
	
	for i in range(0,len(colWith2)-1):
		if(colWith2[i+1]-colWith2[i]==1):
			print("commom index in: ", colWith2[i])
	return PCMatrix


def LTCodeDistribution(N):
	epsilon = 2/3 #for k=10,000 input symbols
	mhu= (epsilon/2) + ((epsilon/2)*(epsilon/2)) # mhu = eps/2 + (eps/2)^2
	D=10 #max-degree=upperBound((4*(1+eps))/eps) 

	#defining coefficients of x^i
	#used round function to roundoff the last digit for non-terminating decimal
	probabilities= [round(mhu/(mhu+1),15)]
	probabilities+=[round(1/((mhu+1)*((i)*(i-1))), 15) for i in range (2,D+1)]
	probabilities+=[round(1/((mhu+1)*D), 15)]
	probabilities+=[0 for i in range (D+2,N+1)]
	su=0
	for i in range(0,len(probabilities)):
		if(i<=12):
			su+=(probabilities[i])
		else:
			break
	return probabilities

#returns the value d for a block i.e degree for any block
def getDegrees(N,c):
	#c=droplet quantity
	#N=k+p
	
	probabilities= LTCodeDistribution(N)
	blocks = [i for i in range(1,int(N)+1)]
	return choices(blocks, weights=probabilities, k=int(c))


class codedBlockStruct: 
	def __init__(self, degree, neighbours, flag): #header might be needed in future
		self.degree=degree
		self.neighbours=neighbours
		self.flag=0 #checks maliciousness of a block
		# self.data=data


#returns indexes for a given block provided degree=d
def getIndex(deg,blocksN):
	indexes= random.sample(range(1,int(blocksN)+1), k=deg)
	return indexes

def writePCMatrix(N,k,d):
	PCMatrix= LDPCParityMatrixGenerator(N,k,d)
	IntermediateBlocks=PCMatrix
	with open("Final Encoded Blocks.csv", "w+") as f:
		f.write("Parity Check Matrix")#Node No., for decoding purpose
		f.write("\n")
		
		for i in range(0,len(IntermediateBlocks)):
			for j in range(0,len(IntermediateBlocks[i])):
				if(j==len(IntermediateBlocks[i])-1):
					f.write(str(IntermediateBlocks[i][j]))	
				else:
					f.write(str(IntermediateBlocks[i][j]) + ",")
			f.write("\n")

	f.close()
	

def LTencoder(N,k,c,NodeNo):
	with open("Final Encoded Blocks.csv", "a") as f:	
		#writing of coded blocks in file
		f.write("Coded Blocks" + "," + str(NodeNo))#Node No., for decoding purpose
		f.write("\n")		

		#Each index i here represents index of intermediate blocks and k original blocks.
		deg = getDegrees(N,c)
		for i in range(c):
			indexes=getIndex(deg[i],12500)
			codedBlock=codedBlockStruct(deg[i],indexes,0)

			###### If handling bitcoin blocks #########
			# codedBlock.data=blocks[indexes[0]]
			# for j in range(1,deg):	
			# 	codedBlock.data= codedBlock.data^blocks[j]
			############################################

			#i writes the index of coded block
			f.write(str(i+1)+ ",")
			for i in range(0, len(codedBlock.neighbours)):
				if(i==len(codedBlock.neighbours)-1):
					f.write(str(codedBlock.neighbours[i]))
				else:
					f.write(str(codedBlock.neighbours[i]) + ",")
			f.write("\n")
	f.close()


############## Call Encoder Function ##################
# writePCMatrix(12500,10000,8)

# T=4000
# while(T):
# 	print(T)
# 	LTencoder(12500,10000,10,T)
# 	T-=1
# print("Done")




########### Decoding ##############
def downloadBlocks(T,NoOfNodesToDownload):
	NodeNo=T
	DownloadedBlocksNo=NoOfNodesToDownload # k(1+epsilon) to be downloaded
	print("NoOfNodes: ",NoOfNodesToDownload)
	DownloadedBlockNodeIndexes = random.sample(range(1,NodeNo +1),k=DownloadedBlocksNo)
	return(DownloadedBlockNodeIndexes)

def removeDegree(block, codedBlocks):
	for codedBlock in codedBlocks:
		for neighbour in codedBlock.neighbours:
			if (block==neighbour):
				codedBlock=codedBlock^block
				codedBlock.degree-=1

def decoder(N, k, NoOfNodesToDownload, totalNodes):
	recoveredBlocks=set()
	downloadedBlocks=NoOfNodesToDownload
	originalBlocks=[]
	IntermediateBlocks=[]
	codedBlocks=[]
	DownloadedBlockNodeIndexes=downloadBlocks(totalNodes, NoOfNodesToDownload)
	
	with open("Final Encoded Blocks.csv", "r") as f:
		reader = csv.reader(f)
		flag=0
		count=0
		print("Downloading blocks")
		for row in reader:
			if("Parity Check Matrix" in row):
				row=next(reader)
				T=2500
				while(T):
					IntermediateBlocks+=[row]
					T-=1

			if(flag==0):
				for i in range(0,len(row)):
					if("Coded Blocks" in row[i]):
						i+=1
						for index in DownloadedBlockNodeIndexes:
							if(str(index)==str(row[i])):
								flag=1

			if(flag==1):
				T=10
				while(T):
					row=next(reader)
					codedBlocks+=[row[1:]]
					T-=1
				flag=0

		print("len downloaded blocks", len(codedBlocks))
		print("Decoding Stage I- Initiated")
		recoveredBlocks=LTDecoder(codedBlocks)
		print("Number of Ist stage recovered blocks: ",len(recoveredBlocks))
		
		print("Decoding Stage II- Initiated")
		originalBlocks=LDPCDecoder(IntermediateBlocks, recoveredBlocks, NoOfNodesToDownload,k)
		print("Number of orginal blocks recovered: ",len(originalBlocks))
	f.close()

	#######writing bootstrap cost in the file#######
	# with open("Bootsrap Cost.csv","a") as f:
	# 	if(len(originalBlocks)==10000):
	# 		f.write(str(NoOfNodes))
	# 		f.write("\n")

def LDPCDecoder(IntermediateBlocks, recoveredBlocks, NoOfNodesDownloaded, k):
	count=0
	NotRecovered=None
	flag=0
	originalBlocks=set()
	
	for block in recoveredBlocks:
		if(int(block) <= (k)):
			originalBlocks.add(block)
	print("pre LDPC orig block len: ",len(originalBlocks))
	while(len(originalBlocks)<(k)):
		flag=0
		for blocks in IntermediateBlocks:
			count=0
			for block in blocks:
				if(block not in recoveredBlocks):
					count+=1
					NotRecovered=block
			if(count==1):
				flag=1
				recoveredBlocks.add(NotRecovered)
				if(int(NotRecovered) <= (k)):
					originalBlocks.add(NotRecovered)
				
		if(flag==0):
			# print("Recalling")
			# decoder(3000,NoOfNodesDownloaded+25)
			break
	return originalBlocks

def LTDecoder(codedBlocks):
	recoveredBlocks=set()
	recoveredBlock=None
	flag=0
	while(len(codedBlocks)>1):
		flag=0
		for blocks in codedBlocks:
			if(len(blocks)==1):
				# print(blocks)
				flag=1
				for block in blocks:
					recoveredBlock=block
				recoveredBlocks.add((recoveredBlock))
				codedBlocks.remove(blocks)
				
				# XORing the block recovered to make more singelton blocks
				for blocks in codedBlocks:
					for block in blocks:
						if(recoveredBlock in blocks):
							blocks.remove(recoveredBlock)
		
		if(flag==0): #no singleton found	
			break
	return recoveredBlocks
decoder(12500, 10000, 1, 1)

# T=1
# while(T):
# 	decoder(12500,650)
# 	T-=1