#!/usr/bin/env python
import os,re,sys

os.system("source /u/apps/root/6.08.00/setroot_CUE.csh")
os.system("setenv PYTHONPATH $ROOTSYS/lib/")
os.system("python -i shms_cal_gui.py")
