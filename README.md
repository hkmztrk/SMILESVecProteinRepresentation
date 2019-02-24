# About SMILESVec based Protein Representation

Here, we represent proteins using their interactings ligands. We utilize SMILES representation of ligands and propose, SMILESVec, which is a ligand representation that is built using  [Word2vec](https://papers.nips.cc/paper/5021-distributed-representations-of-words-and-phrases-and-their-compositionality.pdf) model by Mikolov et al.  

Each SMILES is divided into overlapping subsequences that we call chemical words. Then Word2Vec learns a high-dimensional and real-valued vector for each of these chemical words. SMILES vector is described as the average of the vectors of its chemical word vectors.

We used [Gensim](https://radimrehurek.com/gensim/) implementation  to build word-embeddings.

![Figure](https://github.com/hkmztrk/SMILESVecProteinRepresentation/blob/master/docs/figures/smilesvec.jpg)



****************************************************************
## Installation
### Data 

"data" folder contains the input and output files.
	
"source code" folder contains python source code.

Embeddings files are provided in [here](https://cmpe.boun.edu.tr/~hakime.ozturk/smilesvec.html)


### Requirements

You'll need to install following in order to run the codes.

*   Python 2.7.x or Python 3.x
*   numpy
*   sklearn
*   [chembl_webresource_client](https://github.com/chembl/chembl_webresource_client) 

In order to run the code you have to place an embedding file under ```utils``` folder inside the source folder. 

You can use either  ```drug.l8.chembl23.canon.ws20.txt``` or ```drug.l8.pubchem.canon.ws20.txt```

# Usage

### get SMILESVec for given SMILES
For a list of SMILES strings, it outputs the corresponding SMILESVec.
The following code runs for   ```smiles_sample.txt``` file under utils folder. 
```
python getsmilesvec.py [embedding_file_name]
python getsmilesvec.py drug.l8.chembl23.canon.ws20.txt
```

### get SMILESVec-based representation for given protein (UniProt ID)
For a list of UniProt IDs, it outputs the corresponding SMILESVec-based protein vectors.
The following code runs for  ```prots_sample.txt``` file under utils folder.
```
python getligprotvec.py [embedding_file_name]
python getligprotvec.py drug.l8.pubchem.canon.ws20.txt
```

### How to train your own embeddings of SMILES?

Please refer to [README here](https://github.com/hkmztrk/SMILESVecProteinRepresentation/tree/master/source/word2vec) for detailed information and source code.

### SMILESVec-based Protein Similarity for SCOP A-50
```
will be updated
```

**For citation:**

[A novel methodology on distributed representations of proteins using their interacting ligands](https://academic.oup.com/bioinformatics/article/34/13/i295/5045707) 
```
@article{Ozturk2018Anovel,
author = {Öztürk, Hakime and Ozkirimli, Elif and Özgür, Arzucan},
title = {A novel methodology on distributed representations of proteins using their interacting ligands},
journal = {Bioinformatics},
volume = {34},
number = {13},
pages = {i295-i303},
year = {2018},
doi = {10.1093/bioinformatics/bty287},
URL = {http://dx.doi.org/10.1093/bioinformatics/bty287}

}
```
