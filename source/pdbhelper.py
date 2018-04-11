import requests, re, json, time
import xml.etree.ElementTree as ET

import numpy as np
import pandas as pd
import pickle
from bioservices import *
from chembl_webresource_client.new_client import new_client



PDB_PROT_REST_URL = "http://www.rcsb.org/pdb/rest/customReport?pdbids="
CUSTOM_REPORT = "&CustomReportColumns=db_id"


famc = "50"
case = "fam"
proteinspath="a%s/a%s%s.se.filtered" % (famc, famc, case)
path2mappings="utils/a%s-pdb-unip-chembl.txt" % (famc)
uniprot2chemblmap= "utils/chembl_uniprot_mapping.txt"

pids = [line.split()[0] for line in open(proteinspath)]
fams = [line.split()[1] for line in open(proteinspath)]



def uniprot2chembl_dict(uniprot2chemblmap):
	uniprot2chembl = {}
	with open (uniprot2chemblmap) as f:
		for line in f:
			elements = line.split()

			unip= elements[0]
			chembl = elements[1]

			if unip in uniprot2chembl.keys():
				matches = uniprot2chembl[unip]
				matches.append(chembl)
				matches = list(set(matches))
				uniprot2chembl[unip] = matches
			else:
				matches = []
				matches.append(chembl)
				uniprot2chembl[unip] = matches

	return uniprot2chembl



def get_uniprotid(pdbcode):	
	try:
		uniprotid = []
		response = requests.get(PDB_PROT_REST_URL+pdbcode+CUSTOM_REPORT)
		#print(response)
		root = ET.fromstring(response.content)
		for child in root.iter('dimEntity.db_id'):
			uniprotid.append(child.text)

		return uniprotid

	except requests.exceptions.RequestException as e:
		print(e)
		return "NaN"

def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z


def activity_parser(activities):
	compounds = {}

	for activity in activities:
		cid = activity["molecule_chembl_id"]
		canon_smi = activity["canonical_smiles"]
		#activityval = activity["standard_value"]
		#if activityval < 10000:
		if canon_smi is not None:
		  compounds[cid] = canon_smi
	return compounds

def pdb2chembl_dict(patha50):

	pdb2chembls ={}
	with open(patha50) as f:
		for line in f:
			ids = line.split()
			pdbid = ids[0]
			chemblid = ids[2]

			if pdbid in pdb2chembls.keys():
				chemblids = pdb2chembls[pdbid]
				chemblids.append(chemblid)
				chemblids = list(set(chemblids))
				pdb2chembls[pdbid] = chemblids
			else:
				chemblids = []
				chemblids.append(chemblid)
				pdb2chembls[pdbid] = chemblids
	return pdb2chembls


def get_ligands(pids, filename, dictpath):
	fw = open(filename +".interactions", "w")
	allcompounds = {}
	pdb2chembl = pdb2chembl_dict(dictpath)

	prots = 1
	for i, pid in enumerate(pids):
		if(i % 10 is 0):
			time.sleep(20)

		if pid in pdb2chembl.keys():
			chemblids = pdb2chembl[pid]
			for chemblid in chemblids:
				activities = new_client.activity.filter(target_chembl_id=chemblid) #resjson = s.get_target_bioactivities(chemblid)
				compounds = activity_parser(activities)
				
				if len(compounds) > 0:
				  for comp, smi in compounds.items():
					  fw.write(pid +"\t"+ str(comp) + "\t" + str(smi) + "\n")
					  print(str(prots) + "\t" +pid +"\t"+ str(comp) + "\t" + str(smi))
				  prots +=1
				  #allcompounds = dict(allcompounds.items() + compounds.items())
				  allcompounds = merge_two_dicts(allcompounds, compounds)

	fw.close()

	json.dump(allcompounds, open(filename+".smiles","w"))


def get_db_ids(pids, mappath):
	uniprot2chembl = uniprot2chembl_dict(mappath)

	fw = open(path2mappings,"w")

	for i, pid in enumerate(pids):
		if(i % 100 is 0):
			time.sleep(10)
		#print(i)
		pdbcode = pid[1:5]
		uniprotid = get_uniprotid(pdbcode)

		if uniprotid != "NaN":
			#GET TARGET CHEMBLID and LIGANDS
				for uid in uniprotid:
					chemblids = []

					if "," in uid:
						uids = uid.split()
						for uidd in uids:
							if uidd in uniprot2chembl.keys():
								chemblset = uniprot2chembl[uidd]
								for chemb in chemblset:
									chemblids.append(chemb)
									print(pid +"\t"+uidd + "\t" + chemb)
									fw.write(pid +"\t"+uidd + "\t" + chemb + "\n")

					else:
						if uid in uniprot2chembl.keys():
							chemblset = uniprot2chembl[uid]		
							for chemb in chemblset:
								chemblids.append(chemb)
								print(pid +"\t"+uid + "\t" + chemb)
								fw.write(pid +"\t"+uid + "\t" + chemb + "\n")
	fw.close()



if __name__=="__main__":
	get_db_ids(pids, uniprot2chemblmap) ## produces a three-columned mapping: SCOPEID_UNIPROTID_CHEMBL_TARGET_ID
	get_ligands(pids, proteinspath, path2mappings) ## produces interactions file and ligand SMILES files



