from source import *
from writePCMatrix import *
from LTEncoder import *
from decoder import *


# writePCMatrix(12500, 10000, 8)

def EncodingStageII(T):
	while(T):
		print(T)
		LTencoder(12500,10000,10,T)
		T-=1
	print("Done")

# EncodingStageII(10)
decoder(12500, 10000, 3, 4000)
# T=1
# while(T):
# 	T-=1