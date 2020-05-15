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


Degree distribution used (2x +3x^2)/5

"""

def mod(a):
	if(a>0):
		return a
	else:
		return -a

def constructBinaryMatrix(matrix,PCMatrix):
	for i in range(0,len(PCMatrix)):
		for j in range(0,len(PCMatrix[i])):
			matrix[i][PCMatrix[i][j]]=1

def checkValidColumn(matrix,PCMatrix):
	constructBinaryMatrix(matrix,PCMatrix)	
	tMatrix= np.transpose(matrix)
	for i in range(0,len(tMatrix)):
		count=0
		for j in range(0,len(tMatrix[i])-1):
			if(tMatrix[i][j]==1 and tMatrix[i][j+1]==1):
				count+=1
			if(count>1):
				print("col 1: ",j, " " ,"col 2: ",j+1, end=" ")

def LDPCParityMatrixGenerator(N,k,checkNodeDegree):
	SumC=[0]*(N)
	SumR=[0]*(N-k)
	prevRow=[]
	PCMatrix=[]
	zeroDegreeNode=[i for i in range(0,N)]
	singleDegreeNode=[]
	doubleDegreeNode=[]
	matrix=np.zeros(shape=(N-k,N))
	for i in range (0,N-k):
		countR=0
		PCRow=[]
		for j in range (0, checkNodeDegree):
			flag=1
			while(flag==1):
				if(len(singleDegreeNode)>0):
					col=random.choice(singleDegreeNode)
				elif(len(zeroDegreeNode)>0):
					col=random.choice(zeroDegreeNode)
				else:
					col=random.choice(doubleDegreeNode)
				flag=0
				if(SumC[col]==0):
					singleDegreeNode+=[col]
				if(SumC[col]==3):
					doubleDegreeNode.remove(col)
					flag=1	
				if(col in prevRow): #to check number of 1's common between two rows
					countR+=1
					if(countR>1):
						flag=1
			PCRow+=[col]
			SumC[col]+=1
			SumR[i]+=1
			if(SumC[col]==2):
				doubleDegreeNode+=[col]
				zeroDegreeNode.remove(col)
			if(SumC[col]==2 and col in singleDegreeNode):
				singleDegreeNode.remove(col)
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
	
	checkValidColumn(matrix,PCMatrix)

	return PCMatrix