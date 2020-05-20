from source import *

def LDPCDecoder(N,k,IntermediateBlocks, recoveredBlocks):
	originalBlocks=set()
	NotRecovered=None
	
	for block in recoveredBlocks:
		if(int(block) < (k)):
			originalBlocks.add(block)
	print("pre LDPC decoding, No. of i/p blocks recovered: ",len(originalBlocks))
	
	while(len(originalBlocks)<k):
		flag=0
		for blocks in IntermediateBlocks:
			count=0
			for block in blocks:
				if(block not in recoveredBlocks):
					count+=1
					NotRecovered=block

			if(count==1):
				flag=1
				recoveredBlocks.add(NotRecovered)
				if(int(NotRecovered)<(k)):
					originalBlocks.add(NotRecovered)
				
		if(flag==0):
			break

	print("Number of orginal blocks recovered: ",len(originalBlocks))
	return originalBlocks
