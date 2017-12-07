#!/usr/bin/env python
import time,sys,os,argparse,atexit,subprocess
import ROOT
from ROOT import TH2D,TH2I,gStyle,gPad,TPaveText,TCanvas, TF1
from ROOT import TArrow,TBox,TLine,TDatime,TText,TGFrame
from ROOT import gClient,TGMainFrame,TGVerticalFrame,TGWindow
from ROOT import TGHorizontalFrame,TGLayoutHints
from ROOT import TRootEmbeddedCanvas,TApplication
from ROOT import gROOT, TCanvas

XVALS,YVALS=[],[]
START=0
NCHAN=28


def getScalars():
    zvals=[]
    pzvals=[]
    chan=[]
    pchan=[]
    XVALS[:] = []
    YVALS[:] = []
    
    #file = open("output.txt",'r')
    #row = file.readlines()
    lines = subprocess.check_output(["getscalers","hcvme04"])
    for line in lines.splitlines():
        #print line
    #for line in row:
        info = line.split()
        info[0] = info[0].replace(':', '')
        if info[0].isdigit():
            chan.append(int (info[0])+1)
            info[1] = info[1].rpartition('(')[0]
            zvals.append(float(info[1])/1000)
           
    ix,iy=1,1
    for ii in range (len(zvals)):
        if ii>=START:
            if ii==START+NCHAN : break
            XVALS.append(ix)
            YVALS.append(iy)
            pzvals.append(zvals[ii])
            pchan.append(ii-START+1)
            
            #print pchan[ii-START],
            #print pzvals[ii-START],
            #print XVALS[ii-START],
            #print YVALS[ii-START]
        
            if pchan[ii-START]==14*ix:
                iy=0
                ix+=1
            iy+=1 
    #print 'EndEvent'
    #print len(pzvals),
    #print len(XVALS),
    #print len(YVALS)   
    return pzvals


def calcRates(rates):
    left,right,maximum=0,0,0
    for ii in range(28):#len(XVALS)):
        xx,yy,zz=XVALS[ii],YVALS[ii],rates[ii]
        if xx==1:left+=zz
        else : right+=zz
        if zz>maximum: maximum=zz
    return [left,right,maximum]

def setupHists(hhh):
    for hh in hhh:
        hh.SetStats(0)
        hh.GetXaxis().CenterLabels()
        hh.GetXaxis().SetNdivisions(14,0)
        hh.GetYaxis().CenterLabels()
        hh.GetYaxis().SetNdivisions(16,0)
        hh.GetYaxis().SetTickLength(0)
        hh.GetXaxis().SetTickLength(0)
        hh.GetYaxis().SetTitleOffset(0.5)
        hh.GetXaxis().SetTitleOffset(0.5)
        hh.SetMinimum(0.1)
        xx=1
        for ix in range(2):
            hh.GetXaxis().SetBinLabel(ix+1,'%d'%(xx))
            xx+=1
        yy=14
        for iy in range (14):
            hh.GetYaxis().SetBinLabel(iy+1,'%d'%(yy))
            yy-=1

def makeTime():
    datime=TDatime()
    return '%d/%d/%d %.2d:%.2d:%.2d'%(datime.GetDay(),
             datime.GetMonth(),
             datime.GetYear(),
             datime.GetHour(),
             datime.GetMinute(),
             datime.GetSecond())

def setupPaveTexts(pts):
    for pt in pts:
        pt.SetTextColor(1)
        pt.SetTextAngle(0)
        pt.SetFillColor(0)
        pt.SetBorderSize(0)
        pt.SetLineWidth(0)


#mf=ROOT.TGMainFrame(gClient.GetRoot(),1500,475)
mf=ROOT.TGMainFrame(0,900,925)
gvf=TGVerticalFrame(mf,900,925)
rec=TRootEmbeddedCanvas("ccc",gvf,800,800)
rec2=TRootEmbeddedCanvas("ccc2",gvf,800,25)
gvf.AddFrame(rec,TGLayoutHints(ROOT.kLHintsExpandX|ROOT.kLHintsTop))
gvf.AddFrame(rec2,TGLayoutHints(ROOT.kLHintsExpandX|ROOT.kLHintsBottom))
mf.AddFrame(gvf,TGLayoutHints(ROOT.kLHintsExpandX))
cc=rec.GetCanvas()
cc2=rec2.GetCanvas()
mf.SetEditable(0)
mf.SetWindowName('SHMS PCAL FADC SCALERS')
mf.MapSubwindows()
mf.Resize(901,926)# resize to get proper frame placement
mf.MapWindow()
mf.SetCleanup(ROOT.kDeepCleanup)

def __atexit__():
    del cc2
    del cc
    del rec
    del rec2
    del gvf
    del mf

def main():

    cc.cd()
    cc.SetBorderMode(0)
    cc.SetFixedAspectRatio(1)
    cc.FeedbackMode(1)
    
    gStyle.SetOptStat(0)
    gStyle.SetGridStyle(1)
    gStyle.SetGridColor(11)
    hh=TH2D('hh',';Y;X',2,2,4,14,2,16)
    hi=TH2I('hi',';Y;X',2,2,4,14,2,16)
    setupHists([hh,hi])
    xax,yax=hh.GetXaxis(),hh.GetYaxis()
    hh.Draw('COLZ')
    hi.Draw('TEXTSAME')

    gPad.SetLogz()
    gPad.SetGrid(1,1)
    gPad.SetLeftMargin(0.05)
    gPad.SetRightMargin(0.12)
    
    tt1=TPaveText(0.05,0.94,0.22,1.0,'NDC')
    ttL=TPaveText(0.05,0.905,0.2,0.93,'NDC')
    ttR=TPaveText(0.75,0.905,0.9,0.93,'NDC')
    
    ttLM=TPaveText(2,0.5,2.5,1)
    ttRM=TPaveText(3.5,0.5,4,1)
    
    ttM=TPaveText(0.6,0.94,0.9,1,'NDC')
    ttime=TPaveText(2.8,1.5,3.3,1.9)
    tchan=TPaveText(0,0,0.9,1)
    setupPaveTexts([tt1,ttM,ttime,tchan,ttL,ttR,ttLM,ttRM])
    ttM.SetTextColor(2)

    tarrow=TText(2.9,0.25,'Beam Left')
    arrow=TArrow(2.85,0.5,2.75,0.5,0.02,'|>')
    arrow.SetAngle(40)
    arrow.SetFillColor(1)
    arrow.SetLineWidth(2)
    
    tt=TText()
    tt.SetTextColor(1)
    tt.SetTextAngle(90)
    tt.SetTextSize(0.04)
    tt.DrawText(4.07,9,'kHz')
    tt.SetTextAngle(0)
    tt.SetTextColor(2)
    tt.DrawTextNDC(0.23,0.905,'SHMS PCAL FADC SCALERS')
    ttL.AddText('Left+')
    ttR.AddText('-Right')

    cc.cd()
    for xx in [ttM,tt1,ttL,ttR,arrow,tarrow,ttime,ttLM,ttRM]: xx.Draw()
    cc2.cd()
    tchan.Draw('NDC')
    cc.cd()

    xmin,xmax=xax.GetXmin(),xax.GetXmax()
    ymin,ymax=yax.GetXmin(),yax.GetXmax()
   
    gPad.SetEditable(0)

    while True:

        zvals = getScalars()
       
        for ii in range(len(zvals)):
            hh.SetBinContent(xax.FindBin(XVALS[ii]+1),yax.FindBin(16-YVALS[ii]),zvals[ii])
            hi.SetBinContent(xax.FindBin(XVALS[ii]+1),yax.FindBin(16-YVALS[ii]),zvals[ii])

    
        for xx in [ttime,ttM,tt1,ttLM,ttRM]: xx.Clear()
        [left,right,maximum]=calcRates(zvals)
        tt1.AddText('Total:  %.1f MHz'%((left+right)/1000))
        ttLM.AddText('Left total: %.1f MHz'%(left/1000))
        ttRM.AddText('Right total: %.1f MHz'%(right/1000))
        ttM.AddText('MAX SINGLE CRYSTAL = %.0f kHz'%(maximum))
        ttime.AddText(makeTime())
         
        if not gPad: sys.exit()

        #if gPad.GetEvent()==11:
         #   xy=pix2xy(gPad)
            #ee=ECAL.findChannelXY(xy[0],xy[1])
            #if ee:
         #   tchan.Clear()
            #tchan.AddText(printChannel(ee))
          #  cc2.Modified()
          #  cc2.Update()
        #elif gPad.GetEvent()==12:
         #   tchan.Clear()
          #  cc2.Modified()
           # cc2.Update()
    
   
        cc.Modified()
        cc.Update()

        time.sleep(1)
   

if __name__=='__main__': main()


