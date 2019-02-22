# Traning your own SMILES dataset 

SMILESVec, which is a ligand representation that is built using  [Word2vec](https://papers.nips.cc/paper/5021-distributed-representations-of-words-and-phrases-and-their-compositionality.pdf) model by Mikolov et al.  Each SMILES is divided into overlapping subsequences that we call chemical words. 

		SMILES:  ‘C(C1CCCCC1)N2CCCC2’ 
		words:    ‘C(C1CCCC’, ‘(C1CCCCC’, ‘C1CCCCC1’, ‘1CCCCC1)’, ‘CCCCC1)N’, ‘CCCC1)N2’, …, ’)N2CCCC2’ 

Then Word2Vec learns a high-dimensional and real-valued vector for each of these chemical words. SMILES vector is described as the average of the vectors of its chemical word vectors. This final file is named 'drug.l8.chembl23.canon.ws20.txt' which is trained on SMILES data collected from ChEMBL.

In order to obtain your own file of embeddings from your own training data:

### Requirements

Embeddings files are provided in [here](https://cmpe.boun.edu.tr/~hakime.ozturk/smilesvec.html)
You'll need to install [Gensim](https://radimrehurek.com/gensim/) run  to build word-embeddings.

### Steps 

*    You should provide two SMILES files similar to the ones under "SMILESDATA" folder (train and test). In these files, there is SMILES in each line. Other than ChEMBL, you can use Pubchem or BindingDB to collect SMILES or use your own SMILES data
	
*  Modify 'go.sh' file according to your needs (e.g. name of your SMILES file, length of SMILES words, window size for training).








