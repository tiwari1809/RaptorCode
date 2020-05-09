from source import *

def LTDecoder(codedBlocks):
	recoveredBlocks=set()
	recoveredBlock=None
	flag=0
	while(len(codedBlocks)>1):
		flag=0
		for blocks in codedBlocks:
			if(len(blocks)==1):
				# print(blocks)
				flag=1
				for block in blocks:
					recoveredBlock=block
				recoveredBlocks.add((recoveredBlock))
				codedBlocks.remove(blocks)
				
				# XORing the block recovered to make more singelton blocks
				for blocks in codedBlocks:
					for block in blocks:
						if(recoveredBlock in blocks):
							blocks.remove(recoveredBlock)
		
		if(flag==0): #no singleton found	
			break
	return recoveredBlocks
