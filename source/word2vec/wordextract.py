import sys, json
import re
import os
import  collections
from collections import OrderedDict, defaultdict

letters = ["D" ,"E", "J", "R", "L", "M", "T", "Z" ,"X", "d", "e", "j", "r", "m", "t", "z", "x"]

ELEMENTS = ["He", "Li", "Be", "Ne", "Na", "Mg", "Al", "Si", "Cl", "Ar", "Ca",  "Ti", "Cr", "Mn", "Fe",  
			"Ni", "Cu", "Zn", "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Zr", "Nb", "Tc", "Ru", "Rh", 
			"Pd", "Ag", "Cd", "Sb", "Te", "Xe",  "Ba", "La", "Ce", "Pr", "Nd", "Pm", "Sm", "Eu", "Gd", "Tb", 
			"Dy", "Er", "Tm", "Yb", "Lu", "Hf", "Ta", "Re",  "Ir", "Pt", "Au", "Hg", "Tl", "Pb", "Bi", 
		    "At", "Rn", "Fr", "Ra", "Ac", "Th", "Pa", "Np", "Pu", "Am",  "Bk",  "Es", "Fm", "Md", 
			"Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds", "Rg", "Uut", "Fl", "Uup", "Lv", "Uus", "Uuo"]
			
ExtDir = sys.argv[2] #directory to extract
q= int(sys.argv[3]) #lingosize
protOrLig=sys.argv[4]



def SMILES2LINGO(filename):

	cids = {}
	indexcid = 0
	with open(filename) as f:
		for line in f:
			content = line.split()
			#print(content)
			#comp_id = content[0]
			comp_smi = content[0] #CHNG TO 1
			#print(comp_smi)
			if protOrLig=="p":
				llist = createSeqLists(comp_smi)
			elif protOrLig=="l":
				#llist = getLINGOs(comp_smi, q)
				llist = get_mcs_words(comp_smi)
			writeSMILES(str(indexcid), llist, ExtDir) #comp_id --> indexcid
			#cids[indexcid] = comp_id
			indexcid = indexcid +1
			#print(comp_id)
	#writeIDs("cids_list.txt",cids, "test")
	f.close()
			
			
def modifySMILES(smiles):
	replacements = {}
	matched = 0
	for el in ELEMENTS:
		p = re.compile(el)
		m = p.findall(smiles)
		if m:
			smiles = smiles.replace(el, letters[matched])
			replacements[matched] = el + "," + letters[matched]
			matched = matched +1
	return replacements, smiles

def getLINGOs(smiles, q):
	lingoList = []

	if len(smiles) < q:
		while len(smiles) < q:
			smiles = smiles + "_"
			
	reps, upsmi = modifySMILES(smiles)

	for index in range(len(upsmi)-(q-1)):
		lingo = upsmi[index:index+q]
		if containsFromList(lingo):
			for index in range(len(reps)):
				symbol, letter = reps[index].split(",")
				lingo = lingo.replace(letter,symbol)
		lingoList.append(lingo)

	return lingoList


def createSeqLists(smiles):
  lingoList = {}
  i = 0
  
  if len(smiles) < q:
    while len(smiles) < q:
      smiles = smiles + "_"			
	
  for m in range(q):
    lim = m
    while (lim < len(smiles)):
      lingo = smiles[lim:lim+q]    
      lingoList[i]=lingo
      i += 1
      lim +=q
    lingoList[i] = "\n"
    i +=1
	    
		
def containsFromList(smitext):
	for el in letters:
		m = smitext.find(el)
		if m:
			return True
	return False
	
def equalstoAny(list, p):
	for el in list:
		if p == el:
			return True
	return False


def writeSMILES(filename, lingos, foldername):
	if not os.path.exists(foldername):
		os.makedirs(foldername)

	f = open(os.path.join(foldername , filename + ".txt"), "w+")
	for i in range(len(lingos)):
		f.write(lingos[i] + " ")
	f.close()


def writeIDs(filename, cids, foldername):
	if not os.path.exists(foldername):
		os.makedirs(foldername)

	f = open(os.path.join(foldername , filename + ".txt"), "w+")
	for i in range(len(cids)):
		f.write(cids[i] + " ")
	f.close()



SMILES2LINGO(sys.argv[1]) #smiles filepath
