#!/bin/bash
module load gaussian/gdv
for i in $(ls *.cub); do
	FILE=$PWD/$i
	basename=$(basename $FILE cub)
	cubegen 1 density=scf ${basename}fchk new${i} -1 h TEMP.cub
done
rm TEMP.cub
echo -e '\n Cube files with identical cube origins and gridpoints generated. New files have prefix 'new''
