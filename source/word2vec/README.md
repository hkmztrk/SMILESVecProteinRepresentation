# Traning your own SMILES dataset 

SMILESVec, which is a ligand representation that is built using  [Word2vec](https://papers.nips.cc/paper/5021-distributed-representations-of-words-and-phrases-and-their-compositionality.pdf) model by Mikolov et al.  

Each SMILES is divided into overlapping subsequences that we call chemical words. Then Word2Vec learns a high-dimensional and real-valued vector for each of these chemical words. SMILES vector is described as the average of the vectors of its chemical word vectors.

Here, we generated 'drug.l8.chembl23.canon.ws20.txt' based on SMILES data collected from ChEMBL.


### Steps 

*    "data" folder contains the input and output files.
	
*    "source code" folder contains python source code.

Embeddings files are provided in [here](https://cmpe.boun.edu.tr/~hakime.ozturk/smilesvec.html)


### Requirements

You'll need to install Gensim in order to run the codes.

*   [Gensim](https://radimrehurek.com/gensim/) implementation  to build word-embeddings.



