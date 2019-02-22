export LD_LIBRARY_PATH="/usr/local/lib"
 
TRAINDIR="docs/train/"
TESTDIR="docs/test/"

SMIPATH="SMILESDATA/2MSMILESCan.txt" ## Change here: Include your training data here
SMITESTPATH="SMILESDATA/2MSMILESCan_test.txt" #Change here: Include a smaller test data


for LINGOSize in 8  ## you can change the length of words here
do
	for WINDOWSize in 10 20 ## you can change window size for training 
	do 
			
		rm -r $TRAINDIR
		rm -r $TESTDIR

		awk "BEGIN { print \"Creating LINGOs!!\" }"
		python lingoextract.py $SMIPATH $TRAINDIR $LINGOSize "l"  #training smiles
		python lingoextract.py $SMITESTPATH $TESTDIR $LINGOSize "l"  #test smiles
		awk "BEGIN { print \"Completed creating LINGOs!!\" }"


		cp -a $TESTDIR"." $TRAINDIR

		awk "BEGIN { print \"Word2Vec Training starts..!!\" }"
		python gensimword.py $TRAINDIR $WINDOWSize $LINGOSize


		#awk "BEGIN { print \"Computing IDF values..!!\" }"
		#python comptfidf.py $TRAINDIR
		#mv "utils/idfs.txt" "utils/idfs_l"$LINGOSize"_ws"$WINDOWSize".txt"

   
         done

done

