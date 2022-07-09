#!/bin/bash
module load gaussian/gdv

for i in $(ls -v1 new*.cub); do
	declare -i num=$(ls new*.cub | wc -l)
	file=$(basename $i .cub)
	ffiles+=("$i ")
done

for i in $(ls -1vr new*.cub); do
	rfiles+=("$i ")
done

file=$(printf '%s' "$file" | sed 's/[0-9]*//g')
rawname=${file:3}
prod=$((num/2))
befTS=$((num/2+1))
TS=1
num=$((num-1))
TSf=$file$TS.cub
reactf=$file$num.cub
prodf=$file$prod.cub
befTSf=$file$befTS.cub

echo $befTSf $prodf $reactf $TSf

slice2+=(${rfiles[@]:0:$befTS})
for i in ${!slice2[@]}; do 
	index=$((i+1))
	cubman <<-ADDTEXT
		Su
		${slice2[$i]}
		y
		${slice2[$index]}
		y
		sub$rawname$i.cub
		y
	ADDTEXT
done

slice1+=(${ffiles[@]:0:$prod})
for i in ${!slice1[@]}; do
	index=$((i+1))
	step=$((i+prod))
	cubman <<-ADDTEXT
		SU	
		${slice1[$i]}
		y
		${slice1[$index]}
		y
		sub$rawname$step.cub
		y
	ADDTEXT
done

cubman <<ADDTEXT
SU
$befTSf
y
$TSf
y
sub$rawname$befTS.cub
y	
ADDTEXT

echo -e "\n All subtracted cube files have been generated. Labels correspond to the point along the IRC path. \n"


