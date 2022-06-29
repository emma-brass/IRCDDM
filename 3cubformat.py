#!/usr/bin/env python
import shutil
import math
import glob
import os
import subprocess
dim1=[]
steplst=[]
orilist=[]
for i in glob.glob("*.cub"):
	with open(i, 'r') as f1:
		lines=f1.readlines()
		for line in enumerate(lines):
			dim1=lines[2]
			dim1=dim1.strip().split(' ')
			while '' in dim1: dim1.remove('')
			dim1=[float(elm) for elm in dim1]	
			natoms=int(dim1[0])
			nprev=int(dim1[-1])
			steps1=lines[3:6]
			steps1=''.join(steps1)
			steps1=[[x for x in num.strip().split(' ')] for num in steps1.split('\n')]
			for elm in steps1:
				while '' in elm: elm.remove('')
			steps1.pop()
			steps1=[list(map(float,x)) for x in steps1]
			steps1=[item for sublist in steps1 for item in sublist]
			steplst.append(steps1)
			orilist.append(dim1[1:4])
z=[]
x=[]
y=[]
for i in range(len(orilist)):
	x.append(orilist[i][0])
	y.append(orilist[i][1])
	z.append(orilist[i][2])
origin=[min(x),min(y),min(z)]
origdiff=[float(max(x)-min(x)),float(max(y)-min(y)),float(max(z)-min(z))]
num=[math.ceil(i/steplst[0][1]) for i in origdiff]
for i in range(len(steplst)):
	steplst[i][0]=int(steplst[i][0]+num[0]) 		##may need to change units in other files
	steplst[i][4]=int(steplst[i][4]+num[1])
	steplst[i][8]=int(steplst[i][8]+num[2])
steplst=[item for sublist in steplst for item in sublist]
xstep=steplst[0:4]
ystep=steplst[4:8]
zstep=steplst[8:12]
for i in range(1,len(xstep)):
	xstep[i]="{0:.6f}".format(xstep[i])
for i in range(1,len(ystep)):
	ystep[i]="{0:.6f}".format(ystep[i])
for i in range(1,len(zstep)):
	zstep[i]="{0:.6f}".format(zstep[i])
for i in range(len(origin)):
	origin[i]="{0:.6f}".format(origin[i])
origin=[str(i) for i in origin]
xstep=[str(i) for i in xstep]
ystep=[str(i) for i in ystep]
zstep=[str(i) for i in zstep]
x='   ' .join(xstep)
y='   '.join(ystep)
z='   '.join(zstep)
o='   '.join(origin)
o=str(natoms)+'  '+o+'  '+str(nprev)
with open('TEMP.cub','r') as f:
	lines=f.readlines()
lines[2]='   '+o+'\n'
lines[3]='   '+x+'\n'
lines[4]='   '+y+'\n'
lines[5]='   '+z+'\n'
with open('TEMP.cub','w') as f:
	f.writelines(lines)

print "TEMP.cub file successfully parameterized."
