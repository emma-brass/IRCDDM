#!/usr/bin/env python
import sys
import numpy as np
import os
import subprocess
import re
import array
import shutil
geom=[]
geo=[]
new=[]
dr=os.getcwd()
def symbols():
	symlist=['H','He','Li','Be','B','C','N','O','F','Ne','Na','Mg','Al','Si','P','S','Cl','Ar','K','Ca','Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn','Ga','Ge','As','Se','Br','Kr','Rb','Sr','Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In','Sn','Sb','Te','I','Xe','Cs','Ba','Lu','Hf','Ta','W','Re','Os','Ir','Pt','Au','Hg','Tl','Pb','Bj','Po','At','Rn','Fr','Ra','Lr','Rf','Db','Sg','Bh','Hs','Mt','Ds','Rg','Cn','Nh','Fl','Mc','Lv','Ts','Og'] 
 	return symlist
symlist=symbols()
def NAtoms(filename):
	with open(filename) as f:
       		NAtoms=[]
       		blank=[]
        	for line in f:
        	        if "Number of atoms" in line:
        	                NAtoms=line.split()
        	                for element in NAtoms:
					blank=NAtoms[-1]
					num=int(blank)
        print"Number of atoms:",num
	return num
def findline(filename):
	with open(filename) as f:
		slist=[]
		for num, line in enumerate(f, 1):
			if '1 Geometries' in line:
				slist.append(num)
		return slist
def finalprint(filename):
	with open(filename) as f:
		lines=f.readlines()
		for line in lines:
			cart=[]
			for element in CSlist:
				for i in range(num):
					c=lines[element-1].strip().split()
					del c[0]
					cart.append(c)
					i+=1
					element+=1
	[sublist.append('\n') for sublist in cart]
	return cart
def grepRxCoord(filename,phrase):
	with open(filename) as f:
		lines=f.readlines()
		for i, line in enumerate(lines):
			if phrase in line:
				rxstart=i+1
				rxend=rxstart+2*int(step)//5
				return rxstart,rxend
			else:
				pass

def chrgmult(filename):
	multiplicity=[]
	charge=[]
	with open(filename) as f:
		for line in f: 
			if "Multiplicity" in line: 
				mult=line.split()
				multiplicity=mult[-1]
				multiplicity=int(multiplicity)
			if "Charge " in line: 
				chrg=line.split()
				charge=chrg[-1]
	return multiplicity, charge

def RxCoordfchk(filename):
	rxstart,rxend=grepRxCoord(filename,phrase='Results for each geome')
	with open(filename,'r') as f:
		lines=[]
		for i, line in enumerate(f):
			if i<rxstart:
				pass
			elif rxstart<=i<rxend:
				line=line.strip().split()
				lines.append(line)
				RxCoord=[list(map(float,x)) for x in lines]
				continue
			else:
				break
	RxCoord=[item for sublist in RxCoord for item in sublist]
	RxCoord=[RxCoord[i:i+2] for i in range(0, len(RxCoord), 2)]
	if step//2==step/2:
		TS=int(step//2)
	else:
		TS=int(round((step+1)//2))
	forward=RxCoord[0:TS+2]	
	backward=RxCoord[TS+2:step]
	backward.reverse()
	RxCoord=backward+forward
	if RxCoord[0][0]>RxCoord[-1][0]:
		print "Reaction is exothermic. TS is approximated to be reactant-like in nature."
	else:
		print "Reaction is endothermic. TS is approximated to be product-like in nature."
	return RxCoord
def newfile():
	for count,item in enumerate(new,1):
		chk=''
		current=''
		chk+=newfname+str(count)+'.chk'
		current+=newfname+str(count)+'.gjf'
		with open(current, 'w') as nf:
			nf.write('%chk={} \n#p sp test \n\n{}{} \n\n{} {} \n {} \n\n'.format(chk,newfname,count,multiplicity,charge,item))
		nf.close()
		count+=1
	return nf

def symgrab(filename):
	with open(filename,'r') as f:
		atom=[]
		fatom=[]
		linelist=[]
		lines=f.readlines()
		for i, line in enumerate(lines):
			if "Atomic numbers" in line:
				start=i+1
				end=start+(num//6)
		for i,line in enumerate(lines):
			if i<start:
				pass
			elif start<=i<=end:
				linelist.append(lines[i].split())
	atom=[item for sublist in linelist for item in sublist]
	for i in range(len(atom)):
		for s,sym in enumerate(symlist):
			while atom[i]==s:
				atom[i]=symlist[s-1]
	return atom
def fchk():
	with open(filename, 'r') as f:
		lines=f.readlines()
		l=[]
		geo=[]
		new=[]
		x=[]
		line=lines[slist[0]-1].split()
		digit=int(line[-1])
		step=digit/(3*int(num))	
		n=slist[0]
		for i, line in enumerate(lines):
			if i<n: 
				pass
			elif i>=n:
				geo.append(lines[i].split())
		geo=list(np.ravel(geo[0:(digit//5)]))
		for elm in geo:
			new.append(elm.split('E'))
		for sublist in new:
			for elm in sublist:
				elm=float(elm)
			for i in range(0,len(new)):
				newel=round((float(new[i][0])*0.529177)*10**float(new[i][1]),6) #bohr to angstrom conversion
				l.append(str(newel))	
	l=l[0:digit]
	atom=symgrab(filename)
	atom=step*atom
	l=[l[i:i+3] for i in range(0, len(l), 3)]
	l=[' '.join(subl) for subl in l]
	x=list(zip(atom, l))
	x=[list(i) for i in x]
	x=[' '.join(i) for i in x]
	x=[x[i:i+num] for i in range(0, len(x), num)]
	new=['\n '.join(elm) for elm in x]
	return new
rawfile=raw_input('.fchk file name, excluding file extension: ')
filename=os.path.join(dr,rawfile+'.fchk')
with open(filename,'r') as f:
	lines=f.readlines()	
	for line in lines:
		if "Results for each geom" in line:		
			x=line.strip().split()
			step=int(x[-1])//2
			print "Number of steps:", step
charge,multiplicity=chrgmult(filename)
num=NAtoms(filename)
slist=findline(filename)
new=fchk()
RxCoord=RxCoordfchk(filename)
newfname=raw_input("Name of output file, excluding file extension: \n")
nf=newfile()
