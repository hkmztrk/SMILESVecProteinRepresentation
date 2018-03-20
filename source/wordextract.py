import sys, re, os

letters = ["D" ,"E", "J", "R", "L", "M", "T", "Z" ,"X", "d", "e", "j", "r", "m", "t", "z", "x"]


def loadElements():
	with open('utils/elements.txt') as f:
		element_list = f.read().splitlines()
	f.close()
	return element_list
	
elements = loadElements()

def sequence2LINGO(content, protOrLig, q):
	llist = []

	if protOrLig is "p": #protein
		llist = createSeqLists(content,q)
	elif protOrLig is "l": #ligand
		llist = createLINGOs(content,q)
	return llist
			
			
def modifySMILES(smiles):
	replacements = {}
	matched = 0
	for el in elements:
		p = re.compile(el)
		m = p.findall(smiles)
		if m:
			smiles = smiles.replace(el, letters[matched])
			replacements[matched] = el + "," + letters[matched]
			matched = matched +1
	return replacements, smiles

def createLINGOs(smiles, q):
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

	if len(lingoList) is 0:
		lingoList.append(smiles)

	return lingoList
	
def createSeqLists(smiles, q):
  lingoList = []
  smiles = smiles.upper()

  if len(smiles) < q:
    while len(smiles) < q:
      smiles = smiles + "_"			
	
  for m in range(q):
    lim = m
    while (lim < len(smiles)):
      lingo = smiles[lim:lim+q]    
      lingoList.append(lingo)
   
      lim +=q

	    
  return lingoList

def createCHRs(smiles, protOrLig,  q=1):
	lingoList = []
	upsmi = smiles

	if protOrLig == "p":
		upsmi = upsmi.upper()

	for index in range(len(upsmi)-(q-1)):
		lingo = upsmi[index:index+q]
		lingoList.append(lingo)
	
	return lingoList
		
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




