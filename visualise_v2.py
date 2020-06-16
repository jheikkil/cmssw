import ROOT
import os, shutil, collections
from array import array
ROOT.gROOT.SetBatch(True)
from ROOT import TH1D, TH1F, TLegend, TDirectory
from ROOT import gDirectory, TCanvas, gStyle, gROOT, gPad



sigFile = ROOT.TFile( '/eos/user/j/jheikkil/www/triggerStudies/histos_ele_flat2to100_PU200_eg_v23_BDT.root', 'read' )
bkgFile = ROOT.TFile( '/eos/user/j/jheikkil/www/triggerStudies/histos_nugun_10_PU200_ng_bkg_v3_BDT.root', 'read' )

treeSig = sigFile.Get("sig_train")
treeBkg = bkgFile.Get("bkg_train")

currentBDT = False

version = 'eg_ng_01'

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

numbers = [0] #]

for i in numbers:
        print i
        for variable in variables:
            #histo_name = hist_sig[i]+"_"+variable
            #histo_name_NOMATCH = hist_bkg[i]+"_"+variable

            treeSig.Draw("pt")
            treeBkg.Draw("pt")

            if variable in current:
            #    if i==1:
                #output = variable+"_current_etaLow.png"
            #    elif i==2:
            #       output = variable+"_current_etaHigh.png"
            #    else:
                output = variable+"_current_inc.png"
            else:
                #if i==1:
                #   output = variable+"_new_etaLow.png"
       	       	#elif i==2:
       	       	#   output = variable+"_new_etaHigh.png"
                #else:
                output = variable+"_new_inc.png"

            #print histo_name
            #print histo_name_NOMATCH

            #matched = ROOT.TH1D("mat", "histo2", 4000,0,4000)
            #histotitle = objectPlots[key][1]+"("+cut+")"
            nameSig = variable#+">>matched"
            #print nameSig
            treeSig.Draw("pt")
            matched = gROOT.FindObject("htemp")
            matched.SetTitle(variable)
            matched.SetName("matched")
            #print matched.Integral()

            #nameBkg = variable#+">>NOmatched"
            #treeBkg.Draw(nameBkg)
            #NOmatched = gROOT.FindObject("htemp")
            #NOmatched.SetTitle(variable)
            #NOmatched.SetName("NOmatched")
               #histo2.SetTitle(histotitle)
               #histo2.GetXaxis().SetTitle(objectPlots[key][1])
               #histo2.GetXaxis().SetRangeUser(0,30)
               #histo2.Draw()

               #c.SaveAs(outputDir+output)
            #matched.Integral()

            matched.SetTitle(variable)
            NOmatched.SetTitle(variable)
            if matched.Integral()==0 or NOmatched.Integral()==0: print "ouc", variable, matched.Integral(), NOmatched.Integral() ; continue

            #matched = file.Get(dir+'/'+histo_name)
            #NOmatched = bkg_file.Get(dir+'/'+histo_name_NOMATCH)

            matched.Scale(1.0/matched.Integral(), "width")
            NOmatched.Scale(1.0/NOmatched.Integral(), "width")           

            matched.SetLineColor(1)
            matched.SetLineStyle(1)
            matched.SetLineWidth(3)
  
            NOmatched.SetLineColor(2)
            NOmatched.SetLineStyle(1)
            NOmatched.SetLineWidth(3)

            x1 = 0.15
            x2 = x1 + 0.24
            y2 = 0.90
            y1 = 0.79
            legend = TLegend(x1,y1,x2,y2)
            legend.SetFillStyle(0)
            legend.SetBorderSize(0)
            legend.SetTextSize(0.041)
            legend.SetTextFont(42)
            legend.AddEntry(matched, "Signal",'L')
            legend.AddEntry(NOmatched, "Background",'L')


            #c.SetLogy(0)

            if variable in ['showlenght', 'maxlayer', 'coreshowlenght']:
               matched.GetXaxis().SetRangeUser(0.0,50)
               NOmatched.GetXaxis().SetRangeUser(0.0,50)

            if variable in ['ntc67']:
               matched.GetXaxis().SetRangeUser(0.0,40)
               NOmatched.GetXaxis().SetRangeUser(0.0,40)
  
            if variable in ['ntc90']:
               matched.GetXaxis().SetRangeUser(0.0,70)
               NOmatched.GetXaxis().SetRangeUser(0.0,70)

            if variable in ['meanz']:
               matched.GetXaxis().SetRangeUser(300,400)
               NOmatched.GetXaxis().SetRangeUser(300,400)

            if variable in ['layer10']:
               matched.GetXaxis().SetRangeUser(0.0,20)
               NOmatched.GetXaxis().SetRangeUser(0.0,20)


            if variable in ['layer50', 'layer90']:
               matched.GetXaxis().SetRangeUser(0.0,40)
               NOmatched.GetXaxis().SetRangeUser(0.0,40)

            if variable in ['srrmax', 'srrmean', 'srrtot']:
               matched.GetXaxis().SetRangeUser(0.0,0.03)
               NOmatched.GetXaxis().SetRangeUser(0.0,0.03)
 
            if variable in ['spptot', 'sppmax']:
               matched.GetXaxis().SetRangeUser(0.0,0.2)
               NOmatched.GetXaxis().SetRangeUser(0.0,0.2)
 
            if variable in ['bdteg']:
               matched.GetXaxis().SetRangeUser(-1.0,1.0)
               NOmatched.GetXaxis().SetRangeUser(-1.0,1.0)

            if matched.GetMaximum()>NOmatched.GetMaximum():
                matched.Draw("HIST L")
                NOmatched.Draw("HIST LSAME")
            else:
                NOmatched.Draw("HIST L")
                matched.Draw("HIST L SAME")
            legend.Draw() 

            gStyle.SetOptStat(0)#("ne")
            c.SaveAs(outputDir+output)

            #if 'bdtEg' in variable:
            #    c.SetLogy()    
            #    output = histo_name+"_log.png"
            #    c.SaveAs(outputDir+output)
            #output = histo_name+"_log.png"
            #c.SetLogy()
            #NOmatched.Draw()
            #matched.Draw("SAME")
            #legend.Draw()
            #c.SaveAs(outputDir+output) 
        
c.Close()
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
