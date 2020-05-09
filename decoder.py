from source import *
from downloadBlocks import *
from LTDecoder import *
from LDPCDecoder import *

def decoder(N, k, NoOfNodesToDownload, totalNodes):
	recoveredBlocks=set()
	downloadedBlocks=NoOfNodesToDownload
	originalBlocks=[]
	IntermediateBlocks=[]
	codedBlocks=[]
	DownloadedBlockNodeIndexes=downloadBlocks(NoOfNodesToDownload, totalNodes)
	DownloadedBlockNodeIndexes=[1,3,5]
	with open("test.csv","r") as f:
		reader = csv.reader(f)
		flag=0
		count=0
		print("Downloading blocks")
		for row in reader:
			if("Parity Check Matrix" in row):
				row=next(reader)
				T=2500
				while(T):
					row=next(reader)
					IntermediateBlocks+=[row]
					T-=1

			if(flag==0):
				for i in range(0,len(row)):
					if("Coded Blocks" in row[i]):
						i+=1
						for index in DownloadedBlockNodeIndexes:
							if(str(index)==str(row[i])):
								flag=1

			if(flag==1):
				T=10
				while(T):
					row=next(reader)
					codedBlocks+=[row[1:]]
					T-=1
				flag=0
		print(DownloadedBlockNodeIndexes)
		print("len coded blocks", len(codedBlocks))
		print(codedBlocks)

		# print("Decoding Stage I- Initiated")
		# recoveredBlocks=LTDecoder(codedBlocks)
		# print("Number of Ist stage recovered blocks: ",len(recoveredBlocks))
		
		# print("Decoding Stage II- Initiated")
		# originalBlocks=LDPCDecoder(IntermediateBlocks, recoveredBlocks, NoOfNodesToDownload,k)
		# print("Number of orginal blocks recovered: ",len(originalBlocks))
	f.close()

	#######writing bootstrap cost in the file#######
	# with open("Bootsrap Cost.csv","a") as f:
	# 	if(len(originalBlocks)==10000):
	# 		f.write(str(NoOfNodes))
	# 		f.write("\n")
