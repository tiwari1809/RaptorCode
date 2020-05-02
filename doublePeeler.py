import math
import random
from random import choices
import csv


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


def LTCodeDistribution(N):
	epsilon = 2/3 #for k=10,000 input symbols
	mhu= (epsilon/2) + ((epsilon/2)*(epsilon/2)) # mhu = eps/2 + (eps/2)^2
	D=9 #max-degree=upperBound((4*(1+eps))/eps) 

	#defining coefficients of x^i
	probabilities = [mhu/(mhu+1)]
	probabilities += [1/((mhu+1)*((i)*(i-1))) for i in range (2,int(D)+1)]
	probabilities+=[1/((mhu+1)*D)]
	probabilities += [0 for i in range (int(D)+2,int(N)+1)]
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


def encoder(NodeNo):
	N=12500
	c=10 #for starge saving = 1000
	
	#############  LDPC Encoder  ################
	PCMatrix=[]
	LDPCMatrix(12500, 10000, 8, PCMatrix)
	IntermediateBlocks=[]
	for i in range (0,len(PCMatrix)):
		IntermediateBlocks+=[PCMatrix[i]]
	
	with open("Final Encoded Blocks.csv", "a") as f:
		f.write("Node Number"+ "," + str(NodeNo))
		f.write("\n")

		f.write("IntermediateBlocks")#Node No., for decoding purpose
		f.write("\n")
		
		for i in range(0,len(IntermediateBlocks)):
			for j in range(0,len(IntermediateBlocks[i])):
				if(j==len(IntermediateBlocks[i])-1):
					f.write(str(IntermediateBlocks[i][j]))	
				else:
					f.write(str(IntermediateBlocks[i][j]) + ",")
			f.write("\n")

		
		############## LT Encoder  ################
		
		#writing of coded blocks in file
		f.write("Coded Blocks")#Node No., for decoding purpose
		f.write("\n")		

		#Each index i here represents index from intermediate blocks + k original blocks
		deg = getDegrees(N,c)
		for i in range(int(c)):
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
# T=3000
# while(T):
# 	# print(T)
# 	encoder(T)
# 	T-=1
# print("Done")




########### Decoding ##############
def downloadBlocks(T,NoOfNodes):
	NodeNo=T
	DownloadedBlocksNo=NoOfNodes # k(1+epsilon) to be downloaded
	print("NoOfNodes: ",NoOfNodes)
	DownloadedBlockNodeIndexes = random.sample(range(1,NodeNo +1),k=DownloadedBlocksNo)
	return(DownloadedBlockNodeIndexes)

def removeDegree(block, codedBlocks):
	for codedBlock in codedBlocks:
		for neighbour in codedBlock.neighbours:
			if (block==neighbour):
				codedBlock=codedBlock^block
				codedBlock.degree-=1

def decoder(N, NoOfNodes):
	recoveredBlocks=set()
	downloadedBlocks=NoOfNodes
	originalBlocks=[]
	IntermediateBlocks=[]
	codedBlocks=[]
	DownloadedBlockNodeIndexes=downloadBlocks(3000, NoOfNodes)
	
	with open("Final Encoded Blocks.csv", "r") as f:
		reader = csv.reader(f)
		flag=0
		count=0
		print("Downloading blocks")
		for row in reader:
			if(flag==0):
				for i in range(0,len(row)):
					if("Node Number" in row[i]):
						i+=1
						for index in DownloadedBlockNodeIndexes:
							if(str(index)==str(row[i])):
								flag=1

			if(flag==1):
				count+=1
				T=2500
				row=next(reader)
				while(T):
					row=next(reader)					
					IntermediateBlocks+=[row[1:]]
					T-=1
				T=10
				row=next(reader)
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
		originalBlocks=LDPCDecoder(IntermediateBlocks, recoveredBlocks, NoOfNodes,10000)
		print("Number of orginal blocks recovered: ",len(originalBlocks))
	f.close()
	with open("Bootsrap Cost.csv","a") as f:
		if(len(originalBlocks)==10000):
			f.write(str(D))
			f.write("\n")

def LDPCDecoder(IntermediateBlocks, recoveredBlocks, NoOfNodes, k):
	count=0
	NotRecovered=None
	flag=0
	Count=0
	originalBlocks=set()
	# print(recoveredBlocks)
	if "" in recoveredBlocks:
		recoveredBlocks.remove("")

	for block in recoveredBlocks:
		if(int(block) <= (k)):
			originalBlocks.add(block)
	print("original before LDPC: ",len(originalBlocks))
	while(len(originalBlocks)<(k)):
		flag=0
		print("intermediate: ",len(IntermediateBlocks))
		temp=[]
		for blocks in IntermediateBlocks:
			count=0
			for block in blocks:
				if(block in recoveredBlocks):
					count+=1
					NotRecovered=block
			if(count==7):
				flag=1
				recoveredBlocks.add(NotRecovered)
				temp+=blocks
				if(int(NotRecovered) <= (k)):
					originalBlocks.add(NotRecovered)
				# print("orig blocks: ",len(originalBlocks), end=" ")
				# print(len(originalBlocks),end=" ")
		if(flag==1):
			for blocks in temp:
				IntermediateBlocks.remove(blocks)
				
		print("Flag: ",flag)
		if(flag==0):
			print("Recalling")
			# decoder(3000,NoOfNodes+25)
			break
	print("Singleton LDPC: ",Count)
	return originalBlocks

def LTDecoder(codedBlocks):
	recoveredBlocks=set()
	recoveredBlock=None
	flag=0
	while(len(codedBlocks)>1):
		if(flag==1):
			break
		flag=0
		for blocks in codedBlocks:
			if(len(blocks)==1):
				# print(blocks)
				flag=2
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
			flag=1
			break
	return recoveredBlocks

T=1
while(T):
	decoder(12500,1667)
	T-=1