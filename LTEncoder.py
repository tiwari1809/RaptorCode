from source import *
from LTCodeDegreeDistribution import *

def getDegrees(N,c):#returns the value d for a block i.e degree for any block
	#c=coded blocks(total o/p symbols)
	#N=k+p
	probabilities= LTCodeDegreeDistribution(N)
	degree = [i for i in range(0,int(N))] #degree>D+1 is useless as it has 0 probability 
	return choices(degree, weights=probabilities, k=int(c))


class codedBlockStruct: 
	def __init__(self, degree, neighbours, flag): #header might be needed in future
		self.degree=degree
		self.neighbours=neighbours
		self.flag=0 #checks maliciousness of a block
		# self.data=data


#returns indexes for a given block provided degree=d
def getIndex(deg,N):
	indexes= random.sample(range(0,int(N)), k=deg)
	return indexes

	

def LTencoder(N,k,c,NodeIdentity,gamma):
	fileName="Nodes File Gamma"+ str(gamma)
	with open("%s.csv" %fileName, "a") as f:	
		f.write("Coded Blocks" + "," + str(NodeIdentity))#Node No., for decoding purpose
		f.write("\n")		

		deg = getDegrees(N,c)
		
		for i in range(c):#forming coded blocks
			indexes=getIndex(deg[i],N)
			codedBlock=codedBlockStruct(deg[i],indexes,0)

			# If handling BTC/ETH blocks 
			# codedBlock.data=blocks[indexes[0]]
			# for j in range(1,deg):	
			# 	codedBlock.data= codedBlock.data^blocks[j]
			
			#i writes the index of coded block
			f.write(str(i+1)+ ",")
			for i in range(0, len(codedBlock.neighbours)):
				if(i==len(codedBlock.neighbours)-1):
					f.write(str(codedBlock.neighbours[i]))
				else:
					f.write(str(codedBlock.neighbours[i]) + ",")
			f.write("\n")
	f.close()

