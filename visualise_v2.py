
import ROOT
import os, shutil
from array import array
ROOT.gROOT.SetBatch(True)
from ROOT import TH1D, TLegend
from ROOT import gDirectory, TCanvas, gStyle

file = ROOT.TFile( '/eos/user/j/jheikkil/www/triggerStudies/histos_ele_flat2to100_PU200_eg_v30.root', 'read' )
bkg_file = ROOT.TFile( '/eos/user/j/jheikkil/www/triggerStudies/histos_ele_flat2to100_PU200_eg_v25.root', 'read' )

#bkg_file = ROOT.TFile( '/eos/user/j/jheikkil/www/triggerStudies/histos_ele_flat2to100_PU200_eg_v11.root', 'read' )


currentBDT = False

version = 'v12'

hist_sig = ["h_effNum_HMvDR_all_GEN", "h_effDen_HMvDR_all_GEN", "h_effNum_HMvDR_all_GENPt20", "h_effDen_HMvDR_all_GENPt20"]
hist_bkg = ["h_effNum_HMvDR_all_all", "h_effDen_HMvDR_all_all", "h_effNum_HMvDR_all_Pt20", "h_effDen_HMvDR_all_Pt20"]

version = "GEN_genPart_noReachedEE"

outputDir = '/eos/user/j/jheikkil/www/triggerStudies/'+version+'/'

if os.path.isdir(outputDir)==False:
    os.mkdir(outputDir)
    shutil.copy('/eos/user/j/jheikkil/www/index.php', outputDir)


variables = ['abseta', 'energy', 'eta', 'pt']

dir = 'GenParticleHistos/'
output = ''
#print histo_name
#print histo_name_NOMATCH

c = TCanvas("c", "canvas", 800, 800)
c.cd()

numbers = [0, 1, 2, 3]

names = ["numAll", "denAll", "numPt20", "denPt20"]

for i in numbers:
        print i
        for variable in variables:
            histo_name = hist_sig[i]+"_"+variable
            histo_name_NOMATCH = hist_bkg[i]+"_"+variable

            
            output = variable+"_"+names[i]+".png"

            print histo_name
            print histo_name_NOMATCH
            matched = file.Get(dir+'/'+histo_name)
            NOmatched = bkg_file.Get(dir+'/'+histo_name_NOMATCH)

            #matched.Scale(1.0/matched.Integral(), "width")
            #NOmatched.Scale(1.0/NOmatched.Integral(), "width")           

            matched.SetLineColor(1)
            matched.SetLineStyle(1)
            matched.SetLineWidth(3)
  
            NOmatched.SetLineColor(2)
            NOmatched.SetLineStyle(1)
            NOmatched.SetLineWidth(3)

            x1 = 0.5
            x2 = x1 + 0.24
            y2 = 0.40
            y1 = 0.29
            legend = TLegend(x1,y1,x2,y2)
            legend.SetFillStyle(0)
            legend.SetBorderSize(0)
            legend.SetTextSize(0.041)
            legend.SetTextFont(42)
            legend.AddEntry(matched, "genParts",'L')
            legend.AddEntry(NOmatched, "GEN",'L')


            #c.SetLogy(0)

            if matched.GetMaximum()>NOmatched.GetMaximum():
                matched.SetMinimum(0.0)
                matched.Draw("HIST")
                NOmatched.Draw("HIST SAME")
            else:
                NOmatched.SetMinimum(0.0)
                NOmatched.Draw("HIST")
                matched.Draw("HIST SAME")
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
file.Close()
bkg_file.Close()
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
