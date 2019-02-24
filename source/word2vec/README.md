# Traning your own SMILES dataset 

SMILESVec, which is a ligand representation that is built using  [Word2vec](https://papers.nips.cc/paper/5021-distributed-representations-of-words-and-phrases-and-their-compositionality.pdf) model by Mikolov et al.  Each SMILES is divided into overlapping subsequences that we call chemical words. 

		SMILES:  ‘C(C1CCCCC1)N2CCCC2’ 
		words:    ‘C(C1CCCC’, ‘(C1CCCCC’, ‘C1CCCCC1’, ‘1CCCCC1)’, ‘CCCCC1)N’, ‘CCCC1)N2’, …, ’)N2CCCC2’ 

Then Word2Vec learns a high-dimensional and real-valued vector for each of these chemical words. SMILES vector is described as the average of the vectors of its chemical word vectors. 

The final file containing embedding vectors for each word is named 'drug.l8.chembl23.canon.ws20.txt'. It is trained on about 2M SMILES data collected from ChEMBL.

In order to obtain your own file of chemical word embeddings from your own training data:

### Requirements

*    [Gensim](https://radimrehurek.com/gensim/)  to run Wwrd2vec.

### Steps 

*    You should provide two SMILES files similar to the ones under "SMILESDATA" folder (train and test). In these files, each line contains a single SMILES string. 

*    Other than [ChEMBL](https://www.ebi.ac.uk/chembl/ws), you can use [Pubchem](https://pubchem.ncbi.nlm.nih.gov) or [BindingDB](http://bindingdb.org) to collect SMILES.
	
*  Modify 'go.sh' file according to your needs (e.g. name of your SMILES file, length of SMILES words, window size for training)

		e.g.
		SMIPATH="SMILESDATA/[yourfilename].txt" ## include your training data here
		SMITESTPATH="SMILESDATA/[yourfilename].txt" #include a small test data

*  Modify 'gensimword.py' file according to your needs:

		 e.g. size=100, min_count=1, negative=5, iter=20, sg=1








