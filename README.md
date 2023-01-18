# IRCDDM

## OVERVIEW:
Intrinsic Reaction Coordinate Difference Density Matrices - takes the geometries present in the .fchk file of an IRC calculation and generates individual .gjf files from these. These files are then submitted, and initial .cub files are generated. Following these .cub file generations, the optimal parameters (axis lengths, step sizes, and cube origin) are calculated, and new .cub files are generated for each geometry. This allows for the tracking of electron movement (density) throughout a transition state. 

## Using the Code
```
./IRCDDM.sh 
-> IRC_filename (no extension)
```

### 1fchk.py 
script grabs the geometries present in the .fchk file and generates individual .gjf files. These are created with routeline #p sp test to prevent the creation of the fort.7 file. This calculates the single-point energy for each molecule. Optimizations cannot be performed on these, as this would cause initial and final molecules to "fall back" to the reactant and product geometries. Nosymm keyword is used to prevent unnecessary rotations. 

### 2pybash.sh 
first searches for any unsubmitted files in the current working directory. If present, it submits these files, formats the checkpoint files, and generates the inital unoptimized .cub files. npts is set to -2 (coarse), with 3 points/Bohr. One of these generated .cub files is then copied to a TEMP.cub file for later overwriting and reading of parameters in later steps. 
NOTE: In this step of the script, it is NECESSARY that any files not of interest in the current calculations have corresponding .log files. Additionally, there should be no existing .cub files present in the directory. 

### 3cubformat.py 
reads the parameter lines from each of the generated .cub files and finds the minimum x, y and z for the cube origin. By calculating the change between the minimum present origin and the maximum, the step numbers in each direction are then individually updated. These parameters are then written into the TEMP.cub file. 

### 4chcub.sh 
generates the new .cub files with the updated parameters. The cubegen input line is as follows: cubegen 1 density=scf file.fchk newcubfile.cub -1 h TEMP.cub
This reads the parameters copied into the TEMP.cub file as the parameters for each of the geometries.

### 5subcub.sh 
generates subtracted .cub files between geometries in the IRC path. This includes an option to do iterative subtractions (ith and ith+1) and constant-reference subtractions (reactant and ith point). Currently this necessitates manual user editing of the code, but future edits will include a switch. 

### IRCDDM.sh
calls the previously mentioned scripts.

## Future Work
Adding an option that allows for analysis of single-sided IRC paths (i.e. forward or reverse)
Analysis of changing difference density natural orbitals (DDNOs) is being developed using the existent NBO7 program, which will allow for better understanding of the orbitals of interest in a given IRC pathway.

## Updates
7/11/22: Program now allows for analysis of IRCs having different number of forward/reverse steps. 
\n7/14/22: Initial files now renamed in order of IRC point. 


