from wordextract import *
from cmethods import *
import sys


smiles = sys.argv[1]
emb_file = "data/drug.l8.chembl23.canon.w20.txt"


def loadEmbeddings(LRNPATH):
    embeddings_index = {}

    f = open(os.path.join(LRNPATH)) #'word.11l.100d.txt'
    next(f)
    vsize = 0
    for line in f:
        values = line.split()
        word = values[0]
        vsize = len(values)-1
        coefs = np.asarray(values[1:], dtype='float32')
        embeddings_index[word] = coefs
    f.close()

    return embeddings_index, vsize

EMB, vsize = loadEmbeddings(emb_file)


def getSMIVector(LINGOembds, smiles, q, wordOrChar):


    lingoList = []
    if wordOrChar == "wd":
        lingoList = createLINGOs(smiles, q)
    #elif wordOrChar == "ch":
    #    lingoList = createCHRs(smiles, "l") #ligand, q=1

    smilesVec = vectorAddAvg(LINGOembds, lingoList)
    print(smilesVec)
    return smilesVec


getSMIVector(EMB, smiles, 8, "wd")