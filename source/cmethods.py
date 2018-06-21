import numpy as np
import math



def vectorAdd(LINGOvecs, SMILEStxt):

  vsize = len(LINGOvecs[list(LINGOvecs.keys())[0]])
  sumVec = [float(0) for i in range(vsize)]

  for lingo in SMILEStxt:
    lVecf= [float(0) for j in range(vsize)] 
    if lingo in LINGOvecs:  #TODO:TESTTHIS
      lVec = LINGOvecs[lingo]
      lVecf= [float(j) for j in lVec]

    sumVec = [sumVec[i]+lVecf[i] for i in range(len(lVecf))]
 
  return sumVec

def vectorAddAvg(LINGOvecs, SMILEStxt):

  sumVec = vectorAdd(LINGOvecs, SMILEStxt)
  vecSize = len(SMILEStxt)
  sumVec = [sumVec[i]/vecSize for i in range(len(sumVec))]
  
  return sumVec

def vectorMax(LINGOvecs, SMILEStxt):
	vsize = len(LINGOvecs[list(LINGOvecs.keys())[0]])
	sumVec = [float(0) for i in range(vsize)]
	lVecf= [float(0) for j in range(vsize)]
	for i in range(0,vsize):
		maxi = 0
		for lingo in SMILEStxt:
			if lingo in LINGOvecs:
				lVec = LINGOvecs[lingo]
				lVecf= [float(j) for j in lVec]
				if lVecf[i] > maxi:
					maxi = lVecf[i]
	
		sumVec[i] = maxi
	
	return sumVec

def vectorFreq(SMILEStxt1, SMILEStxt2):

	lset1 = list(set(SMILEStxt1))
	lset2 = list(set(SMILEStxt2))

	common =0
	sim =0
	for lingo in lset1:
		freq1= SMILEStxt1.count(lingo)
		freq2=0

		if lingo in lset2:
			freq2 = SMILEStxt2.count(lingo)
			common +=1
		tanimoto = 1 - (math.fabs(freq1-freq2) / math.fabs(freq1 + freq2))  
		sim += tanimoto


	denom = len(lset1) + len(lset2) - common #CHECK THIS
    
	return sim/denom

def vectorFreq2(SMILEStxt1, SMILEStxt2):

	lset1 = list(set(SMILEStxt1))
	lset2 = list(set(SMILEStxt2))

	uniques = list(set(SMILEStxt1 + SMILEStxt2))

	sim =0
	for lingo in uniques:
		freq1= SMILEStxt1.count(lingo)
		freq2 = SMILEStxt2.count(lingo)

		tanimoto = 1 - (math.fabs(freq1-freq2) / math.fabs(freq1 + freq2))  
		sim += tanimoto

	denom = len(uniques)
    
	return sim/denom


def vectorMin(LINGOvecs, SMILEStxt):
	vsize = len(LINGOvecs[list(LINGOvecs.keys())[0]])
	sumVec = [float(0) for i in range(vsize)]
	lVecf= [float(0) for j in range(vsize)]
	for i in range(0,vsize):
		mini = float('inf')
		for lingo in SMILEStxt:
			if lingo in LINGOvecs:
				lVec = LINGOvecs[lingo]
				lVecf= [float(j) for j in lVec]
				if lVecf[i] < mini:
					mini = lVecf[i]
	
		sumVec[i] = mini
	
	return sumVec
	
def vectorMinMax(LINGOvecs, SMILEStxt):
	vectormin = vectorMin(LINGOvecs, SMILEStxt)
	vectormax = vectorMax(LINGOvecs, SMILEStxt)
	
	return np.append(vectormax, vectormin, axis=0)
