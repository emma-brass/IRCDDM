#!/bin/bash
module load gaussian/gdv
#add a part of the code that will append all current files in the directory to a list. 
#if a file is in a list, then it will NOT be submitted

for i in $(ls *.gjf); do
        FILE=$PWD/$i
	filename=$(basename $FILE gjf)
	if ! [[ -f "${filename}log" ]]; then	
		gsub $i
		files+="$filename "
	fi
done
sleep 7

echo $files
for i in $files; do
	formchk ${i}chk
	cubegen 1 density=scf ${i}fchk ${i}cub -2 h
done

for i in $(ls *.qlog *.sub); do
	rm $i
done

for i in $(ls *.cub);
do
	cp $i TEMP.cub
done
echo -e "\n TEMP.cub file for later parameter manipulation generated.\n"
