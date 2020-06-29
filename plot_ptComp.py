import ROOT
import os, shutil, collections
from array import array
ROOT.gROOT.SetBatch(True)
from ROOT import TH1D, TH1F, TLegend, TDirectory
from ROOT import gDirectory, TCanvas, gStyle, gROOT, gPad


sigFile = ROOT.TFile( '/eos/user/j/jheikkil/www/triggerStudies/histos_ele_flat2to100_PU200_eg_MC_v31_BDT.root', 'read' )
sigFile2 =  ROOT.TFile( '/eos/user/j/jheikkil/www/triggerStudies/histos_ele_flat2to100_PU200_eg_MC_v31_BDT_lowpt.root', 'read' )

bkgFile = ROOT.TFile( '/eos/user/j/jheikkil/www/triggerStudies/histos_nugun_10_PU200_ng_bkg_v3_BDT.root', 'read' )
bkgFile2 = ROOT.TFile( '/eos/user/j/jheikkil/www/triggerStudies/histos_nugun_10_PU200_ng_bkg_v3_BDT_lowpt.root', 'read' )

treeSig = sigFile.Get("sig_train")
treeSig2 = sigFile2.Get("sig_train")

treeBkg = bkgFile.Get("bkg_train")
treeBkg2 = bkgFile2.Get("bkg_train")

currentBDT = False

cuts = [
         ["low", "eta>1.5 && eta<=2.7"], ["high", "eta>2.7 && eta<=3.0"], ["inc", ""]	 
       ]

nameCut = cuts[0][0]
etaCut = cuts[0][1]

version = 'eg_ng_03_MC_comp_'+nameCut

outputDir = '/eos/user/j/jheikkil/www/triggerStudies/'+version+'/'

if os.path.isdir(outputDir)==False:
    os.mkdir(outputDir)
    shutil.copy('/eos/user/j/jheikkil/www/index.php', outputDir)


variables = ['pt', 'eta', 'absEta', 'phi', 'energy', 'nclu', 'showerlength', 'coreshowerlength', 
             'firstlayer', 'maxlayer', 'seetot', 'seemax', 'spptot', 'sppmax', 'srrtot', 'srrmax', 
             'srrmean', 'meanz', 'szz', 'emaxe', 'layer10', 'layer50', 'layer90', 'ntc67', 'ntc90', 'hoe', 'bdteg']

current = ['coreshowerlength','showerlength','firstlayer','maxlayer','szz','srrmean','srrtot','seetot','spptot']

output = ''
#print histo_name
#print histo_name_NOMATCH

c = TCanvas("c", "canvas", 800, 800)
c.cd()

#cut = "eta>1.5 and eta<=2.7"
#cut = "eta>2.7 and eta<=3.0"

for variable in variables:

    if variable in current:
        output = variable+"_current.png"
    else:
        output = variable+"_new.png"

    histoname = variable
   
    if variable in ['bdteg']:
        name = variable+">>"+histoname+"(100,-1,1)"
    else:
        name = variable+">>"+histoname

    if len(etaCut)>0:
        treeSig.Draw(name, etaCut)
    else:
        treeSig.Draw(name)
    signal = gROOT.FindObject(histoname)
    #c.GetListOfPrimitives().ls()
    signal.SetTitle(histoname)
    signal.SetName(histoname)
    signal.Scale(1.0/signal.Integral(), "width")
    #c.GetListOfPrimitives().ls()

    histoname2 = variable+"__"
    if variable in ['bdteg']:
        name2 = variable+">>"+histoname2+"(100,-1,1)"
    else:
	name2 = variable+">>"+histoname2

    if len(etaCut)>0:
        treeSig2.Draw(name2, etaCut)
    else:
       	treeSig2.Draw(name2)

    signal2 = gROOT.FindObject(histoname2)
    #c.GetListOfPrimitives().ls()
    signal2.SetTitle(histoname2)
    signal2.SetName(histoname2)
    signal2.Scale(1.0/signal2.Integral(), "width")
  #  c.GetListOfPrimitives().ls()

    histonameBKG = variable+"_"
    if variable in ['bdteg']:
        name3 = variable+">>"+histonameBKG+"(100,-1,1)"
    else:
       	name3 = variable+">>"+histonameBKG

    if len(etaCut)>0:
        treeBkg.Draw(name3, etaCut)
    else:
       	treeBkg.Draw(name3)
    bkg = gROOT.FindObject(histonameBKG)
    #c.GetListOfPrimitives().ls()
    bkg.SetTitle(variable)
    bkg.SetName(histonameBKG)
    bkg.Scale(1.0/bkg.Integral(), "width")
   # c.GetListOfPrimitives().ls()

    histonameBKG2 = variable+"___"
    if variable in ['bdteg']:
        name4 = variable+">>"+histonameBKG2+"(100,-1,1)"
    else:
        name4 = variable+">>"+histonameBKG2

    if len(etaCut)>0:
        treeBkg2.Draw(name4, etaCut)
    else:
	treeBkg2.Draw(name4)
    bkg2 = gROOT.FindObject(histonameBKG2)
    #c.GetListOfPrimitives().ls()
    bkg2.SetTitle(variable)
    bkg2.SetName(histonameBKG2)
    bkg2.Scale(1.0/bkg2.Integral(), "width")
    #c.GetListOfPrimitives().ls()
    

    if variable in ['bdteg']:
        signal.GetXaxis().SetRangeUser(-1.0,1.0)
        signal2.GetXaxis().SetRangeUser(-1.0,1.0)
        bkg.GetXaxis().SetRangeUser(-1.0,1.0)
        bkg2.GetXaxis().SetRangeUser(-1.0,1.0)

    if variable in ['pt']:
        signal.GetYaxis().SetRangeUser(0, 1.05*bkg2.GetMaximum())
        #signal2.GetXaxis().SetRangeUser(0, 30.0)
        #bkg.GetXaxis().SetRangeUser(0, 30.0)

    signal.SetLineColor(1)
    signal.SetLineStyle(1)
    signal.SetLineWidth(3)

    signal2.SetLineColor(4)
    signal2.SetLineStyle(1)
    signal2.SetLineWidth(3)

    bkg.SetLineColor(2)
    bkg.SetLineStyle(1)
    bkg.SetLineWidth(3)

    bkg2.SetLineColor(8)
    bkg2.SetLineStyle(1)
    bkg2.SetLineWidth(3)

    x1 = 0.5
    x2 = x1 + 0.24
    y2 = 0.82
    y1 = 0.69
    legend = TLegend(x1,y1,x2,y2)
    legend.SetFillStyle(0)
    legend.SetBorderSize(0)
    legend.SetTextSize(0.041)
    legend.SetTextFont(42)
    legend.AddEntry(signal, "sig, high pt",'L')
    legend.AddEntry(bkg, "bkg, high pt",'L')
    legend.AddEntry(signal2, "sig, low pt", 'L')
    legend.AddEntry(bkg2, "bkg, low pt", 'L')

    #c.GetListOfPrimitives().ls()
    #name2 = variable+">>htemp2"
    #treeBkg.Draw(name2)
    #bkg = gROOT.FindObject("htemp2")
    #bkg.SetTitle("htemp2")
    #bkg.SetName("htemp2")
    #bkg.Scale(1.0/bkg.Integral(), "width")
    #c.GetListOfPrimitives().ls()

    if signal.GetMaximum()>bkg.GetMaximum() and signal.GetMaximum()>bkg2.GetMaximum() and signal.GetMaximum()>signal2.GetMaximum():
        signal.Draw("HIST")
        signal2.Draw("HIST SAME")
        bkg.Draw("HIST SAME") 
        bkg2.Draw("HIST SAME")
    elif signal.GetMaximum()>bkg.GetMaximum() and signal2.GetMaximum()>bkg2.GetMaximum() and signal2.GetMaximum()>signal.GetMaximum():
        signal2.Draw("HIST")
        signal.Draw("HIST SAME")
        bkg.Draw("HIST SAME")
        bkg2.Draw("HIST SAME")
    elif bkg.GetMaximum()>bkg2.GetMaximum():
        bkg.Draw("HIST ")
        bkg2.Draw("HIST SAME")
        signal2.Draw("HIST SAME")
        signal.Draw("HIST SAME")    
    else:
        bkg2.Draw("HIST ")
        bkg.Draw("HIST SAME")
        signal2.Draw("HIST SAME")
        signal.Draw("HIST SAME")
    legend.Draw()
    #sigFile.cd()
    #signal.Draw("HIST")
    #bkgFile.cd()
    #bkg.Draw("HIST SAME")
    gStyle.SetOptStat(0)
    c.SaveAs(outputDir+output)

sigFile.Close()
bkgFile.Close()
#dir = file.GetDirectory("Cluster3DHistos")
#file.cd("Cluster3DHistos")
#dir.cd()
#gDirectory.ls()
#file.Reset()
#file.SetDirectory(0)
#dirList = file.GetListOfKeys()
#print dirList
#file.cd("Cluster3DHistos")
#file.GetListOfKeys().Print()
#for key in file.GetListOfKeys():
#    print "-------------------------"
#    kname = key.GetName()
#    print kname
#    hists = key.ReadObj().GetListOfKeys()
#    for histo in hists:
#        print histo.GetName()
    #key.ls()	
    #key.ReadObj().GetName()
    #kname.GetList()
    #for hah in key.GetListOfKeys():
    #    print "jes"
    #   print histo.GetName()
