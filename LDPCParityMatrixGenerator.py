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

"""

def mod(a):
	if(a>0):
		return a
	else:
		return -a

def LDPCParityMatrixGenerator(N,k,checkNodeDegree):
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
		for j in range (0, checkNodeDegree):
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
		if(mod(colWith2[i+1]-colWith2[i])==1):
			print("commom index in: ", colWith2[i])
	return PCMatrix
