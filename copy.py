import ROOT as r

#___________________________________________________________

#inputFileName = "/eos/user/j/jheikkil/www/triggerStudies/histos_pion_flat2to100_PU200_eg_v24.root"
inputFileName = "/eos/user/j/jheikkil/www/triggerStudies/histos_ele_flat2to100_PU200_eg_v25.root"
#inputFileName="/eos/user/j/jheikkil/www/triggerStudies/histos_nugun_10_PU200_ng_bkg_v3.root"
outputTrain = inputFileName.replace(".root", "_BDT.root")

inputFile = r.TFile.Open(inputFileName)
outputFileTRAIN = r.TFile.Open(outputTrain, "recreate")
outputFileTRAIN.cd()

dirName = "Cluster3DHistos"

if "PU200_eg" in inputFileName: 
   signalTree = "h_cl3d_HMvDR_all_Pt20" #GENPt
   bkgTree = "h_cl3d_HMvDR_all_all_noMatch" #GEN
elif "histos_nugun" in inputFileName:
   signalTree = "NAN"
   bkgTree = "h_cl3d_HMvDR_Pt20_noMatch"
else:
   signalTree = "NAN"
   bkgTree = "NAN"
fracTrain = 0.9

sigPT = 10.0
bkgPT = 20.0

for k in inputFile.GetListOfKeys() :
    if dirName in k.GetName():
       dir = inputFile.Get(k.GetName())
       for j in dir.GetListOfKeys():
           print "dealing with: ", j.GetName()
           if signalTree==j.GetName():
               cutPT = sigPT
               nameTrain = "sig_train"
               nameTest = "sig_test"
           elif bkgTree==j.GetName():
               cutPT = bkgPT
               nameTrain = "bkg_train"
               nameTest = "bkg_test"
           else: continue
           origTree = inputFile.Get(dir.GetName()+"/"+j.GetName())
           cut = "pt>"+str(cutPT)
           #dummyTree = origTree.CopyTree()
           print "Total number of events to be processed: ", origTree.GetEntries()
           print "Preparing the dummy tree, our cut is: ", cut
           dummyTree = origTree.CopyTree(cut)
           #for i in range(origTree.GetEntries()):
           #    origTree.GetEntry(i)
           #    if i % 1000 == 1000: print "Processed event ", i
           #    if origTree.pt>cutPT:
           #        dummyTree.Fill(origTree.GetEntry(i))

           print "I have produced the dummy tree, moving on to the actual trees"
           newTrain=dummyTree.CloneTree(0)
           newTrain.SetName(nameTrain)
           newTest=dummyTree.CloneTree(0)
           newTest.SetName(nameTest)

           nEv = dummyTree.GetEntries()
           nTrain = int(fracTrain*nEv)
           nTest = nEv-nTrain

           print "here we go: ", nEv, nTrain, nTest

           for i in range(nEv):
               dummyTree.GetEntry(i)
               if i % 1000 == 1000: print "Processed event ", i
               if i<nTrain:
                   newTrain.Fill(dummyTree.GetEntry(i))
               else: 
                   #print "Moving on to the testing tree"
                   newTest.Fill(dummyTree.GetEntry(i))
           newTrain.Write()
           newTest.Write()
               

#outputFileTRAIN.Write()
outputFileTRAIN.Close()

