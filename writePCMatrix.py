from source import *
from LDPCParityMatrixGenerator import *

def writePCMatrix(N,k,checkNodeDegree):
	PCMatrix= LDPCParityMatrixGenerator(N,k,checkNodeDegree)
	IntermediateBlocks=PCMatrix
	with open("test.csv", "w+") as f:
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
