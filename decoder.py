from source import *
from downloadBlocks import *
from LTDecoder import *
from LDPCDecoder import *

totalDownloadedBlocks=0
totalDownloadedBlocksNodeIndex=[]
prevT=50
def checkDecoded(N,k, c,additionalDownload,totalNodes, originalBlocks, gamma):
	global totalDownloadedBlocks
	global totalDownloadedBlocksNodeIndex
	global prevT
	if(len(originalBlocks)<k):
		print("Decoding failed")
		decoder(N,k, c,additionalDownload,totalNodes, gamma, prevT)
		totalDownloadedBlocks+=50
	else:
		fileName="Bootstrap Cost Gamma"+ str(gamma)
		with open("%s.csv" %fileName, "a") as f:
			f.write(str(totalDownloadedBlocks))
			f.write("\n")

def decoder(N, k, c, NoOfNodesToDownload, totalNodes, gamma, T):
	global totalDownloadedBlocks
	global totalDownloadedBlocksNodeIndex
	global prevT
	if(T!= prevT):
		totalDownloadedBlocks=0
		totalDownloadedBlocksNodeIndex=[]
		totalRecoveredBlocks=set()
	prevT=T
	recoveredBlocks=set()
	downloadedBlocks=NoOfNodesToDownload
	originalBlocks=[]
	IntermediateBlocks=[]
	codedBlocks=[]
	DownloadedBlockNodeIndexes=downloadBlocks(NoOfNodesToDownload, totalNodes, totalDownloadedBlocksNodeIndex)
	totalDownloadedBlocks+=NoOfNodesToDownload
	totalDownloadedBlocksNodeIndex+=DownloadedBlockNodeIndexes
	fileName="Nodes File Gamma"+ str(gamma)
	with open("%s.csv" %fileName,"r") as f:
		reader = csv.reader(f)
		flag=0
		count=0
		print("Downloading blocks")
		for row in reader:
			if("Parity Check Matrix" in row):
				T=N-k
				while(T):
					row=next(reader)
					IntermediateBlocks+=[row]
					T-=1
			if(flag==0):
				for i in range(0,len(row)):
					if("Coded Blocks" in row[i]):
						i+=1
						for index in totalDownloadedBlocksNodeIndex:
							if(str(index)==str(row[i])):
								flag=1

			if(flag==1):
				T=c
				while(T):
					row=next(reader)
					codedBlocks+=[row[1:]]
					T-=1
				flag=0
		print("Downloaded blocks: ", len(codedBlocks))

		print("Decoding Stage I- Initiated")	
		recoveredBlocks=LTDecoder(codedBlocks)
	
		print("Decoding Stage II- Initiated")
		originalBlocks=LDPCDecoder(N,k,IntermediateBlocks, recoveredBlocks)
		checkDecoded(N,k, 1,10,totalNodes, originalBlocks, gamma)
	f.close()