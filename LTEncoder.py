from source import *
from LTCodeDegreeDistribution import *

#returns the value d for a block i.e degree for any block
def getDegrees(N,c):
	#c=droplet quantity
	#N=k+p
	
	probabilities= LTCodeDegreeDistribution(N)
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

	

def LTencoder(N,k,c,NodeNo):
	with open("test.csv", "a") as f:	
		#writing of coded blocks in file
		f.write("Coded Blocks" + "," + str(NodeNo))#Node No., for decoding purpose
		f.write("\n")		

		#Each index i here represents index of intermediate blocks and k original blocks.
		deg = getDegrees(N,c)
		for i in range(c):
			indexes=getIndex(deg[i],12500)
			codedBlock=codedBlockStruct(deg[i],indexes,0)

			# If handling bitcoin blocks 
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

