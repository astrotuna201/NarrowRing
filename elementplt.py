#!/usr/bin/env python
##### !/usr/local/bin/python
##### !/usr/bin/python # for DPH mac
###### last updated by Lucy Lu Sep27, 2018
import numpy as np
import math
import os
import matplotlib.pyplot as plt
import sys 
import glob
from math import log10, floor
from decimal import *
import matplotlib.cm as cm
import random
from scipy.interpolate import interp1d
from hnread import *
from center_angle import *
from plotScatter import *
from chkEle import *
from getEle import *

def checkinput(argv):                                                                       
    programname = sys.argv[0]                                                               
    if len(argv) != 4:  # Exit if not exactly one arguments  
    	print '---------------------------------------------------------------------------'                               
        print "This program plots sample particle element vs time for a ring based on hnbody body files.\n It takes into 3 arguments:\n Argument 1: the folder name\n Argument 2: element to plot ('a','e','i',etc.. [see chkEle.py for more info]. You can also put in 'r' or 'z')\n Argument 3: how many particles to plot\n"
	print ' '
	print ' Example:    '+programname+' m1 e 10'  
	print '---------------------------------------------------------------------------'                                    
        sys.exit(1)                                                                         
    gridfile = argv[1]                                                                                                                                    
    if not os.path.isdir(gridfile):  # Exit if folder does not exist                  
        print 'ERROR: unable to locate folder ' + gridfile                             
        sys.exit(1)   

checkinput(sys.argv)


## how many particles to plot
ptp=int(sys.argv[3])
## element number
elem=str(sys.argv[2])
ele_n=geteleInd(str(sys.argv[2]))


path=sys.argv[1] ## put second input into file 
pathname=str(path)
print pathname
if pathname[-1]=="/":
	path=pathname[0:-1]

# count and sort files
numfile=0
filename=[]
filenumb=[]
for file in glob.glob(os.path.join(path,'body*.dat')):
	numfile+=1
	filename_one =(file.split('/'))[-1]
	filename.append(str(file))
	filenumb.append(filename_one.split('y')[-1].split('.')[-2])

filenumb, filename = zip(*sorted(zip([int(i) for i in filenumb],filename)))
#print filenumb
#print filenumb
#print filename
#print filenumb
filetp = filename[0:len(filename):int(round(float(len(filename))/float(ptp)))]
filenp = filenumb[0:len(filename):int(round(float(len(filename))/float(ptp)))]
#print filenp
#print filetp

realN=len(filetp)
if realN!=ptp:
	print "Optimized to plot "+ str(len(filetp))+" plots instead of "+str(ptp)+" plots!"
	
#print filetp

# set up plot numbers
mp=[]
for i in range(realN+1):
	if i==0:
		continue
	elif float(realN)/float(i) - int(float(realN)/float(i)) == 0:
		mp.append(i)

#print mp

if realN**0.5-int(realN**0.5)==0:
	subplotNumR=int(realN**0.5)
	subplotNumC=int(realN**0.5)	
elif len(mp)==2:
	if mp[-1] < 10:
		subplotNumR=mp[-1]
		subplotNumC=1
	else:
		subplotNumR=int(math.ceil(float(realN)**0.5))
		subplotNumC=subplotNumR
else:
	#print "mp not 2"
	if mp[int(np.floor(len(mp)/2.))]==mp[int(np.ceil(len(mp)/2.))]:
		subplotNumR=mp[int(np.floor(len(mp)/2.))-1]
		subplotNumC=mp[int(np.ceil(len(mp)/2.))]
	else:
		subplotNumR=mp[int(np.floor(len(mp)/2.))]
		subplotNumC=mp[int(np.ceil(len(mp)/2.))]
	
	if abs(subplotNumR-subplotNumC) > 6:
		subplotNumR=int(math.ceil(float(realN)**0.5))
		subplotNumC=subplotNumR

#print subplotNumR
#print subplotNumC

#print subplotNum
fig, axes = plt.subplots(nrows=subplotNumR, ncols=subplotNumC,figsize=(1.3*realN, 1.3*realN/(float(subplotNumC)/float(subplotNumR))))
subplotnumber=1
for file in filetp:
	plt.subplot(subplotNumR,subplotNumC,subplotnumber)
	#print getEle(file,"t")
	if elem=='r':
		a = getEle(file,'a')
		e = getEle(file,'e')
		nu = getEle(file,'nu')
		plt.plot(getEle(file,"t"),a*(1.-e*e)/(1.+e*np.cos(nu*d2r)))
	elif elem=='z':
		a = getEle(file,'a')
		e = getEle(file,'e')
		cw = getEle(file,'cw')
		nu = getEle(file,'nu')
		i = getEle(file,'i')
		W = getEle(file,'W')
		plt.plot(getEle(file,"t"),a*(1.-e*e)/(1.+e*np.cos(nu*d2r))*np.sin(i*d2r)*np.sin((cw-W+nu)*d2r))
	else:
		plt.plot(getEle(file,"t"),getEle(file,elem))
	plt.xlabel('Time [yr]')
	plt.ylabel(str(sys.argv[2])+str(filenp[subplotnumber-1]))
	#print subplotnumber
	subplotnumber=subplotnumber+1

#fig.suptitle(str(sys.argv[2])+"vs time for "+str(len(filetp))+" particles", fontsize=ptp*2)	
#fig.tight_layout() # 
plt.savefig(path+"/element_"+str(sys.argv[2])+"_"+str(len(filetp))+".png")	
#plt.show()
