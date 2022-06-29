#!/bin/bash
module load gaussian/gdv

echo -e "\n(troubleshooting tip 1: if there are .cub files missing for large molecule/large step IRC paths, try increasing the sleep time between job submissions and checkpoint file formatting)"
echo -e "\n(troubleshooting tip 2: this program will NOT format the checkpoint file for the IRC job. If you would like to read the geometries from the .fchk file, it must be formatted prior to starting this program)"
echo e "\n(troubleshooting tip 3: in order to optimize the desired .cub files, make sure that there are no currently present in the working directory.)"
echo -e "\n  . . . . . Opening . . . . .  \n"
python 1fchk.py  ###generates the .gjf files from the IRC, then deletes irc.fchk and irc.chk to prevent irc.cub gen
bash 2pybash.sh   ###submits the previously made .gjf files, then formchks them and generates the initial .cub file
python 3cubformat.py ##generates optimal .cub file parameters for ALL points along the IRC - steps in each direction + origin
bash 4chcub.sh ##submit new job for each .cub file by reading in temp.cub parameterized file
bash 5subcub.sh

echo -e "\n Gaussian cubman program must be called by the user for the generation of difference density matrices. \nUse format cubman Su [file1.cub] [file2.cub]. Make sure to use the cubefiles with optimized origins and axes, designated with prefix "new" \n"
rm TEMP.cub
echo -e "\n . . . . . Closing . . . . . \n"

