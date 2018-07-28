# About SMILESVec based Protein Representation



![Figure](https://github.com/hkmztrk/SMILESVecProteinRepresentation/blob/master/docs/figures/smilesvec.jpg)

SMILESVec representations are built based on [Word2vec](https://papers.nips.cc/paper/5021-distributed-representations-of-words-and-phrases-and-their-compositionality.pdf) model by Mikolov et al. Gensim implementation was used to build word-embeddings.

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
