from source import *

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

Edge Degree distribution: (2x +3x^2)/5

"""

def constructBinaryMatrix(matrix,PCMatrix):
	SumC=[0]*(12500)
	SumR=[0]*(2500)
	for i in range(0,len(PCMatrix)):
		for j in range(0,len(PCMatrix[i])):
			matrix[i][PCMatrix[i][j]]=1
	for i in range(0,len(matrix)):
		for j in range(0,len(matrix[i])):
			if(matrix[i][j]==1):
				SumC[j]+=1
				SumR[i]+=1
	for s in SumR:
		if(s!=13):
			print("row sum error")
	for s in SumC:
		if(s<2 or s>3):
			print("col sum error")		

def checkValidColumn(matrix,PCMatrix):
	constructBinaryMatrix(matrix,PCMatrix)	
	tMatrix= np.transpose(matrix)
	for i in range(0,len(tMatrix)-1):
		count=0
		for j in range(0,len(tMatrix[i])):
			if(tMatrix[i][j]==1 and tMatrix[i+1][j]==1):
				count+=1
			if(count>1):
				print("More than one 1's in common between columns")
				print("col 1: ",j, " " ,"col 2: ",j+1, end=" ")

def LDPCParityMatrixGenerator(N,k,checkNodeDegree):
	SumC=[0]*(N)
	SumR=[0]*(N-k)
	prevRow=[]
	PCMatrix=[]
	countC=0
	index=[i for i in range(0,N)]
	doubleDegreeNode=[]
	matrix=np.zeros(shape=(N-k,N))
	for i in range (0,N-k):
		countR=0
		PCRow=[]
		for j in range (0, checkNodeDegree):
			flag=1
			while(flag==1):
				if(len(index)>0):
					col=random.choice(index)
				else:
					col=random.choice(doubleDegreeNode)
				flag=0
				if(col in prevRow): #to check number of 1's common between two rows
					countR+=1
					if(countR>1):
						flag=1
				if(col in PCRow):
					flag=1
				if(SumC[col]==2 and countC>=7500):
					flag=1
				if(SumC[col]==3 and flag==0):
					doubleDegreeNode.remove(col)
					flag=1	
				
			PCRow+=[col]
			SumC[col]+=1
			SumR[i]+=1
			if(SumC[col]==2):
				doubleDegreeNode+=[col]
				index.remove(col)
			if(SumC[col]==3):
				countC+=1
		prevRow=[]
		prevRow+=[PCRow]
		PCMatrix+=[PCRow]
	count=0
	for s in SumC:
		if(s==3):
			count+=1
	print("Nodes with degree 3: ",count)
	count=0
	for s in SumC:
		if(s==2):
			count+=1
	print("Nodes with degree 2: ",count)
	count=0
	for s in SumR:
		if(s!=13):
			count+=1
			print("s: ",s)
	print("No. of check nodes with degree!=13: ",count)
	
	checkValidColumn(matrix,PCMatrix)

	return PCMatrix