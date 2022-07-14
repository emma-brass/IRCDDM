#!/bin/bash
module load gaussian/gdv

cd optimized_cubes

for i in $(ls -v1 new*.cub); do
	declare -i num=$(ls new*.cub | wc -l)    ###sets num variable to total number of new*.cub files
	file=$(basename $i .cub)
	xfiles+=("$i ")
done

file=$(printf '%s' "$file" | sed 's/[0-9]*//g') ###removes step number from file name
rawname=${file:3}    ### gets user-inputted raw file name (no extension/numbers)
echo ${xfiles[@]}

for i in ${!xfiles[@]}; do
	index=$((i+1))		
	cubman <<-ADDTEXT
		Su
		${xfiles[$i]}
		y
		${xfiles[$index]}
		y
		sub$rawname$i.cub
		y
	ADDTEXT
done
mkdir sub_cubes

for i in $(ls sub*.cub); do
	mv $i sub_cubes
done
