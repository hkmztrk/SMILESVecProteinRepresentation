#DIRNAME=$(date +%Y%m%d_%H%M%S)
#mkdir "docs" #$DIRNAME
mkdir "outputs" #$DIRNAME
#mkdir "data" #$DIRNAME


LRNDRUGLINGO8="data/word/drug.l8.chembl23.canon.ws20.txt" 
LRNDRUGCHR1="data/char/drug.chembl.canon.l1.ws20.txt"
LRNDRUGCHR1Pub="data/char/drug.pubchem.canon.l1.ws20.txt"

LRNPROTLINGO="data/word/prot.l3.w20.100d.txt"
LRNPROTCHR="data/char/prot.w25.d100.txt"

SEQFILE="a50/a50fam.se.filtered" 
PAIRList="a50/xac"
SMILESFILE="a50/a50fam.se.filtered.smiles"

INTERACTIONFILE="a50/a50fam.se.filtered.interactions"

MODELCHOICE=2
ldrugLen=8
lprotLen=3
SMICHOICE=2

#Arguments: LRNPATH, pairfile, proteinspath, wordChar, protOrLig, q, MODELCHOICE 
##ProtVec

awk "BEGIN { print \"Computing similarity list..!!\" }"
python lingosim.py $LRNPROTLINGO $PAIRList $SEQFILE "wd" "p" $lprotLen $MODELCHOICE 


#SMILESVec

awk "BEGIN { print \"Computing similarity list..!!\" }"
python lingosmi.py $LRNDRUGLINGO8Pub $PAIRList $SMILESFILE "wd" "l" $ldrugLen  $INTERACTIONFILE $SMICHOICE #MODEL AVG

$SHELL
