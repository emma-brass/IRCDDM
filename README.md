# IRCDDM

OVERVIEW:
Intrinsic Reaction Coordinate Difference Density Matrices - takes the geometries present in the .fchk file of an IRC calculation and generates individual .gjf files from these. These files are then submitted, and initial .cub files are generated. Following these .cub file generations, the optimal parameters (axis lengths, step sizes, and cube origin) are calculated, and new .cub files are generated for each geometry. This allows for the tracking of electron movement (density) throughout a transition state. 

1fchk.py script grabs the geometries present in the .fchk file and generates individual .gjf files. These are created with routeline #p sp test to prevent the creation of the fort.7 file. This calculates the single-point energy for each molecule. Optimizations cannot be performed on these, as this would cause initial and final molecules to "fall back" to the reactant and product geometries

2pybash.sh first searches for any unsubmitted files in the current working directory. If present, it submits these files, formats the checkpoint files, and generates the inital unoptimized .cub files. npts is set to -2 (coarse), with 3 points/Bohr. One of these generated .cub files is then copied to a TEMP.cub file for later overwriting and reading of parameters in later steps. 
NOTE: In this step of the script, it is NECESSARY that any files not of interest in the current calculations have corresponding .log files. Additionally, there should be no existing .cub files present in the directory. 

3cubformat.py reads the parameter lines from each of the generated .cub files and finds the minimum x, y and z for the cube origin. By calculating the change between the minimum present origin and the maximum, the step numbers in each direction are then individually updated. These parameters are then written into the TEMP.cub file. 

4chcub.sh generates the new .cub files with the updated parameters. The cubegen input line is as follows: cubegen 1 density=scf file.fchk newcubfile.cub -1 h TEMP.cub
This reads the parameters copied into the TEMP.cub file as the parameters for each of the geometries.

IRCDDM.sh calls the previously mentioned scripts. This is created for simplicity so that only one script needs to be called by the user. 

CURRENT WORK: 
5subcub.sh will generate subtracted .cub files between the ith and i+1th geometries in the IRC path. First, however, it is necessary to confirm the order of points in the IRC (i.e. file1 corresponds to reactant, and the last numbered file corresponds to the product). 
This will use the cubman Gaussian utility with input line as follows: cubman Su file1.cub y file2.cub y output.cub y

ADDED 7/8/22
5subcub.sh generates subtracted .cub files using the Gaussian cubman utility for the nth and nth+1 steps in an IRC path. These are generated from reactant to product, with files being named consecutively in this order. Output subtracted files have name format sub$original_name$step.cub. 
Note - while this section of the code provides extensive visualization for the changes over the reaction coordinate, the comparison of individual (i.e. non-consecutive) points of interest is still possible via manual input. 



