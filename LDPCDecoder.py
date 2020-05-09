from source import *

def LDPCDecoder(IntermediateBlocks, recoveredBlocks, NoOfNodesDownloaded, k):
	count=0
	NotRecovered=None
	flag=0
	originalBlocks=set()
	
	for block in recoveredBlocks:
		if(int(block) <= (k)):
			originalBlocks.add(block)
	print("pre LDPC orig block len: ",len(originalBlocks))
	while(len(originalBlocks)<(k)):
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
				if(int(NotRecovered) <= (k)):
					originalBlocks.add(NotRecovered)
				
		if(flag==0):
			# print("Recalling")
			# decoder(3000,NoOfNodesDownloaded+25)
			break
	return originalBlocks
