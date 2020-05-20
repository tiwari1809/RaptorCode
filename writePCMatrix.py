from source import *
from LDPCParityMatrixGenerator import *

def writePCMatrix(N,k,checkNodeDegree,gamma):
	PCMatrix= LDPCParityMatrixGenerator(N,k,checkNodeDegree)
	IntermediateBlocks=PCMatrix
	fileName="Nodes File Gamma"+ str(gamma)
	with open("%s.csv" %fileName, "w+") as f:
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
