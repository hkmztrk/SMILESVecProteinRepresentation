import sys, os, math
from scipy import spatial
from collections import Counter
import numpy as np
from wordextract import *
from scipy.linalg import norm
from scipy.spatial.distance import euclidean
import json

OutputDir = "outputs/"
#LRNPATH = sys.argv[1]
#PAIRFILE = sys.argv[2]
#SEQPATH=sys.argv[3] 
#wordChar=sys.argv[4] 
#protOrLig=sys.argv[5] 
#q=int(sys.argv[6])


#loadEmbeddingsv2(sys.argv[1])
	
def loadEmbeddings(LRNPATH):
    embeddings_index = {}

    f = open(os.path.join(LRNPATH)) #'word.11l.100d.txt'
    vsize = 0
    for line in f:
        values = line.split()
        word = values[0]
        vsize = len(values)-1
        coefs = np.asarray(values[1:], dtype='float32')
        embeddings_index[word] = coefs
    f.close()

    return embeddings_index, vsize

	


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

	
def SMILESVectorSim(LINGOVecs, smi1f, smi2f, VCHOICE): # main function to handle similarity functions

  choice = VCHOICE
  
  if(choice == 0):
    v1= vectorAdd(LINGOVecs,smi1f)
    v2= vectorAdd(LINGOVecs,smi2f)
    return hellingerDist(v1, v2)
  elif(choice == 1):
    v1= vectorAddAvg(LINGOVecs,smi1f)
    v2= vectorAddAvg(LINGOVecs,smi2f)
    return cosineSim2(v1, v2)
    #return hellingerDist(v1, v2)
  elif(choice == 2): # TO DO FREQ VECTOR
    return vectorFreq2(smi1f, smi2f)
  elif(choice == 3):
    v1= vectorMax(LINGOVecs,smi1f)
    v2= vectorMax(LINGOVecs,smi2f)
    return cosineSim(v1, v2)
  elif(choice == 4):
    v1= vectorMin(LINGOVecs,smi1f)
    v2= vectorMin(LINGOVecs,smi2f)
    return cosineSim(v1, v2)
  elif(choice == 5):
    v1= vectorMinMax(LINGOVecs,smi1f)
    v2= vectorMinMax(LINGOVecs,smi2f)
    return cosineSim(v1, v2)
  else:
    print("add:0, avg:1, freq:2, max:3, min:4")
	
		
def cosineSim(vec1, vec2):   #TODO: own cosine sim

  vec1f = [float(i) for i in vec1]
  vec2f = [float(i) for i in vec2]
  result = 1 - spatial.distance.cosine(vec1f, vec2f)
  
  return result

def cosineSim2(vec1, vec2):
	return np.dot(vec1, vec2)/(np.linalg.norm(vec1)* np.linalg.norm(vec2))

_SQRT2 = (1 /np.sqrt(2))     # sqrt(2) with default precision np.float64

def hellingerDist(vec1, vec2):

	summ =0
	for i, val in enumerate(vec1):

		v1r = math.sqrt(math.fabs(vec1[i]))
		v2r = math.sqrt(math.fabs(vec2[i]))
		s1p = math.pow((v1r-v2r),2)
		summ += s1p
	return  1 - (math.sqrt(summ) * _SQRT2)


def formatsim(score):
 sims_out= '{:.10f}'.format(score)
 simsst= str(sims_out).replace("00000000","0")
 
 return simsst

def write2txt(name, listt):
	fs = open(name,"w")

	for p in listt:
		fs.write(p)

	fs.close()



  
def constructSim(LINGOembdspath, pairfile, proteinspath, wordChar, protOrLig, q, VCHOICE):   # text file folder & pair list
	if not os.path.exists(OutputDir):
		os.makedirs(OutputDir)

	sequences = {}
	LINGOembds, vsize = loadEmbeddings(LINGOembdspath)

	with open(proteinspath) as fr:
		for line in fr:
			ptuples = line.split()
			sequences[ptuples[0]] = ptuples[2].strip()
	fr.close()

	vname = pairfile[4:-4]	
	f = open(os.path.join(OutputDir, vname +  "_" + str(VCHOICE)+ "_simmat.txt"), "w")
	
	with open(pairfile) as fr:
		for line in fr:
			
			pairs = line.split()
			bioid = pairs[0]
			bioid2 = pairs[1]
			biotxt1=[]
			biotxt2=[]

			if wordChar == "wd": ## TODO creating LINGOS
				biotxt1 = sequence2LINGO(sequences[bioid], protOrLig, q)
				biotxt2 = sequence2LINGO(sequences[bioid2], protOrLig, q)
			elif wordChar == "ch":
				biotxt1 = createCHRs(sequences[bioid], protOrLig)
				biotxt2 = createCHRs(sequences[bioid2], protOrLig)


			sims = SMILESVectorSim(LINGOembds, biotxt1, biotxt2, VCHOICE)
			simsst = formatsim(sims)
			print(simsst)
			
			f.write(bioid + "\t" + bioid2 + "\t" + str(simsst) + "\n")
		
	
	f.close()
	
constructSim(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], int(sys.argv[6]), int(sys.argv[7])) #folder path & pair file 

##constructSim function should be commented while running ligand based

#(LRNPATH, pairfile, proteinspath, wordChar, protOrLig, q, MODELCHOICE) 









