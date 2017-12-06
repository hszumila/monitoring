#!/usr/bin/env python
import time,sys,os,argparse,atexit,subprocess


XVALS,YVALS=[],[]
chan=[]

def getScalars():
    zvals=[]

#    os.system('getscalers hcvme04')
    lines = subprocess.check_output(["getscalers","hcvme04"])
    for line in lines.splitlines(): 

    #file = open("output.txt",'r')
    #row = file.readlines()
    
    #for line in row:
        info = line.split()
        info[0] = info[0].replace(':', '')
        if info[0].isdigit():
            chan.append(int (info[0])+1)
            info[1] = info[1].rpartition('(')[0]
            zvals.append(float(info[1])/1000)
    ix,iy=1,1
    for ii in range (len(zvals)):
        XVALS.append(ix)
        YVALS.append(iy)

        print chan[ii],
        print zvals[ii],
        print XVALS[ii],
        print YVALS[ii]
        
        if chan[ii]==16*ix:
            iy=0
            ix+=1
        iy+=1       
    return zvals


getScalars()
