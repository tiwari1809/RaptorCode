from source import *

def LTCodeDegreeDistribution(N):
	epsilon = 2/3 #for k=10,000 input symbols
	mhu= (epsilon/2) + ((epsilon/2)*(epsilon/2)) # mhu = eps/2 + (eps/2)^2
	D=10 #max-degree=upperBound((4*(1+eps))/eps) 

	#defining coefficients of x^i
	#used round function to roundoff the last(15th) digit for non-terminating decimal
	probabilities= [0,round(mhu/(mhu+1),15)]
	probabilities+=[round(1/((mhu+1)*((i)*(i-1))), 15) for i in range (2,D+1)]
	probabilities+=[round(1/((mhu+1)*D), 15)]
	probabilities+=[0 for i in range (D+2,N)]
	su=0
	for i in range(0,len(probabilities)):
		if(i<=12):
			su+=(probabilities[i])
		else:
			break
	return probabilities