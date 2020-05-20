from source import *

def downloadBlocks(NoOfNodesToDownload, totalNodes, preDownloaded):
	NodeNo=totalNodes
	DownloadedBlocksNo=NoOfNodesToDownload # k(1+epsilon) to be downloaded
	nodeIndex=[i for i in range(1,NodeNo+1)]
	if(len(preDownloaded)>0):
		for block in preDownloaded:
			if(block in nodeIndex):
				nodeIndex.remove(block)
	DownloadedBlockNodeIndexes = random.sample(nodeIndex,k=DownloadedBlocksNo)
	return(DownloadedBlockNodeIndexes)