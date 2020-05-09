from source import *

def downloadBlocks(NoOfNodesToDownload, totalNodes):
	NodeNo=totalNodes
	DownloadedBlocksNo=NoOfNodesToDownload # k(1+epsilon) to be downloaded
	DownloadedBlockNodeIndexes = random.sample(range(1,NodeNo +1),k=DownloadedBlocksNo)
	return(DownloadedBlockNodeIndexes)
