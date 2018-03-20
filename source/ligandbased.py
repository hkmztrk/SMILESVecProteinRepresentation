import sys, os, math, json
from scipy import spatial
from collections import Counter
import numpy as np
from wordextract import *
from protbased import *

OutputDir = "outputs/"

SMIFile = sys.argv[3]
SMILESDict = json.load(open(SMIFile)) 
maccspath="data/a50fam.se.filtered.tab.seperated.maccs.binary"
maccsDict = {}


#LINGOembds, vsize = LINGOvector(trainedSMIWords) #trained word vectors file 

def loadInteractions(dfilename):    
    
    dic = {}
    with open(dfilename) as f:
        for line in f:
            if line.strip():
                darr = line.split()
                elist = []
                if (darr[0] not in dic.keys()):
                    elist.append(darr[1])
                    dic[darr[0]] = elist
            
                elif (darr[0] in dic.keys()): ## and (darr[0] in proteins)
                    nlist = dic[darr[0]]
                    nlist.append(darr[1])
                    dic[darr[0]] = nlist
    
    f.close()
    return dic
    
def getSMIVector(LINGOembds, ligand, q, wordOrChar):
    smiles = SMILESDict[ligand]

    lingoList = []
    if wordOrChar == "wd":
        lingoList = createLINGOs(smiles, q)
    elif wordOrChar == "ch":
        lingoList = createCHRs(smiles, "l") #ligand, q=1

    smilesVec = vectorAddAvg(LINGOembds, lingoList)

    return smilesVec

proteinVectors = {}
proteinVectorsFreq = {}
proteinVectorsMACCS = {}

def chooseProtSMIVector(bioid, bioid2, trainedEmbds, protligdic, q, wordOrChar, opt):

    simsst = 0

    if opt == "1":
        biotxt1= []
        biotxt2= []
        if bioid not in proteinVectors.keys():
            biotxt1 = getProtSMIVector(trainedEmbds, protligdic,  bioid, q, wordOrChar)
        else:
            biotxt1= proteinVectors[bioid]

        if bioid2 not in proteinVectors.keys():
            biotxt2 = getProtSMIVector(trainedEmbds, protligdic,  bioid2, q, wordOrChar)
        else:
            biotxt2 = proteinVectors[bioid2]

        sims = cosineSim(biotxt1, biotxt2)
        simsst = formatsim(sims)

    elif opt == "2":
        biotxt1= []
        biotxt2= []

        if bioid not in proteinVectorsFreq.keys():
            biotxt1 = getProtSMIFreq(protligdic,  bioid, q, wordOrChar)
        else:
            biotxt1= proteinVectorsFreq[bioid]

        if bioid2 not in proteinVectorsFreq.keys():
            biotxt2 = getProtSMIFreq(protligdic,  bioid2, q, wordOrChar)
        else:
            biotxt2 = proteinVectorsFreq[bioid2]

        sims = vectorFreq2(biotxt1, biotxt2)    
        simsst = formatsim(sims)

    elif opt == "3":

        biotxt1= []
        biotxt2= []

        if bioid not in proteinVectorsMACCS.keys():
            biotxt1 = getProtSMIMACCS(protligdic,  bioid, maccsDict)
        else:
            biotxt1= proteinVectorsMACCS[bioid]

        if bioid2 not in proteinVectorsMACCS.keys():
            biotxt2 = getProtSMIMACCS(protligdic,  bioid2, maccsDict)
        else:
            biotxt2 = proteinVectorsMACCS[bioid2]

        sims = cosineSim(biotxt1, biotxt2)    
        simsst = formatsim(sims)

    return simsst


def getProtSMIVector(LINGOembds, protlig, protein, q, wordOrChar):
    sumVec = [float(0) for i in range(100)]

    if protein in protlig.keys():
        ligands = protlig[protein]
        
        for ligand in ligands:
            ligVec = getSMIVector(LINGOembds, ligand, q, wordOrChar)
            sumVec = [sumVec[i]+ligVec[i] for i in range(len(ligVec))]

        sumVec = [sumVec[i]/len(ligands) for i in range(len(sumVec))]
    else:
        print(protein)
    
    proteinVectors[protein] = sumVec
    return sumVec




def getProtSMIFreq(protlig, protein, q, wordOrChar):

    smiList = []

    if protein in protlig.keys():
        ligands = protlig[protein]

        for ligand in ligands:
            smiles = SMILESDict[ligand]
            lingoList = []
            if wordOrChar == "wd":
                lingoList = createLINGOs(smiles, q)
            elif wordOrChar == "ch":
                lingoList = createCHRs(smiles, "l") #ligand, q=1

            #TODO FILL IN SMILIST
            smiList = smiList + lingoList
    else:
        print(protein)


    proteinVectorsFreq[protein] = smiList

    return smiList

def getProtSMIMACCS(protlig, protein, maccsDict):

    sumVec = [float(0) for i in range(166)]
    lcounter = 0

    if protein in protlig.keys():
        ligands = protlig[protein]

        for ligand in ligands:
            vec = [float(0) for i in range(166)]
            if ligand in maccsDict.keys():
                vec = maccsDict[ligand]
                sumVec = [sumVec[i]+vec[i] for i in range(len(vec))]
                lcounter +=1

    else:
        print(protein)
    
    sumVec = [sumVec[i]/lcounter for i in range(len(sumVec))]

    proteinVectorsMACCS[protein] = sumVec

    return sumVec


#python lingosmi.py $LRNDRUGLINGO $PAIRList $SMILESFILE "wd" "l" $ldrugLen  $INTERACTIONFILE

def constructSimMatrixv2(embFile, pairfile, wordOrChar, protOrLig, q, ifile, opt):   # text file folder & pair list
    if not os.path.exists(OutputDir):
        os.makedirs(OutputDir)

    trainedEmbds, x = loadEmbeddings(embFile)
    
    protligdic = loadInteractions(ifile)
    f = open(os.path.join(OutputDir,  ifile[0:3] + "_smi_simmat.txt"), "w+")
    counter=1
    with open(pairfile) as fr:
        for line in fr:
            print("pairs ", str(counter))
            pairs = line.split()
            bioid = pairs[0]
            bioid2 = pairs[1]

            simsst = chooseProtSMIVector(bioid, bioid2, trainedEmbds, protligdic,  q, wordOrChar, opt)

            print(simsst)

            counter +=1
            
            f.write(bioid + "\t" + bioid2 + "\t" + str(simsst) + "\n")
        
    
    f.close()
    



constructSimMatrixv2(sys.argv[1], sys.argv[2], sys.argv[4], sys.argv[5], int(sys.argv[6]),  sys.argv[7], sys.argv[8]) # pair file 








