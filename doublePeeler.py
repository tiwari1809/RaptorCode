from source import *
from writePCMatrix import *
from LTEncoder import *
from decoder import *


#writePCMatrix takes input in order: N,k, checkNodeDegree, gamma
# writePCMatrix(5000, 4000, 13, 4000)


#LT encoder takes input in order: N,k, c, gamma, T=Node Identity
def EncodingStageII(T):
	while(T):
		# print(T)
		LTencoder(5000,4000,1,T,4000)
		T-=1
	print("Done")
# EncodingStageII(10000)


#decoder takes input in order: N, k, c, Bootstrap Cost, Total Nodes in system, gamma, T
T=1
while(T):
	print("Entry Number: ",T)
	decoder(5000, 4000, 1, 5500, 10000, 4000, T)
	T-=1
