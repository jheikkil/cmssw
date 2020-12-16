import FWCore.ParameterSet.Config as cms

l1PhaseIITree = cms.EDAnalyzer("L1PhaseIITreeStep1Producer",

   egTokenBarrel = cms.InputTag("L1EGammaClusterEmuProducer","","MENUTREE"),
   tkEGTokenBarrel = cms.InputTag("L1TkElectronsEllipticMatchCrystal","EG", "MENUTREE"),
   tkEMTokenBarrel = cms.InputTag("L1TkPhotonsCrystal","EG","MENUTREE"),

   egTokenHGC = cms.InputTag("l1EGammaEEProducer","L1EGammaCollectionBXVWithCuts","MENUTREE"),
   tkEGTokenHGC = cms.InputTag("L1TkElectronsEllipticMatchHGC","EG","MENUTREE"),
   tkEMTokenHGC = cms.InputTag("L1TkPhotonsHGC","EG","MENUTREE"),

   muonKalman = cms.InputTag("simKBmtfDigis","BMTF", "MENUTREE"),
   muonOverlap = cms.InputTag("simOmtfDigis","OMTF", "MENUTREE"),
   muonEndcap = cms.InputTag("simEmtfDigis","", "MENUTREE"),
   TkMuonToken = cms.InputTag("L1TkMuons","","MENUTREE"),

   #Global muons
   muonToken = cms.untracked.InputTag("simGmtStage2Digis", "", "MENUTREE"),
   TkGlbMuonToken = cms.InputTag("L1TkGlbMuons","", "MENUTREE"),


 #  ak4L1PF = cms.InputTag("ak4PFL1PuppiCorrected"),

   l1pfPhase1L1TJetToken  = cms.InputTag("Phase1L1TJetCalibrator" ,   "Phase1L1TJetFromPfCandidates", "MENUTREE"), # not there yet either


   caloTauToken = cms.InputTag("L1CaloJets","CaloTaus", "MENUTREE"),

   l1PFMet = cms.InputTag("l1PFMetPuppi", "", "MENUTREE"),

   zoPuppi = cms.InputTag("l1pfProducerBarrel","z0","MENUTREE"),
   l1vertextdr = cms.InputTag("VertexProducer","l1vertextdr","MENUTREE"),
   l1vertices = cms.InputTag("VertexProducer","l1vertices","MENUTREE"),
   l1TkPrimaryVertex= cms.InputTag("L1TkPrimaryVertex","","MENUTREE"),

   L1NNTauToken = cms.InputTag("l1NNTauProducerPuppi","L1PFTausNN","MENUTREE"),
   L1NNTauPFToken = cms.InputTag("l1NNTauProducer","L1PFTausNN","MENUTREE"),

   tkTrackerJetToken = cms.InputTag("L1TrackJets", "L1TrackJets", "MENUTREE"),
   tkMetToken = cms.InputTag("L1TrackerEtMiss","L1TrackerEtMiss", "MENUTREE"),
   tkMhtTokens = cms.VInputTag( cms.InputTag("L1TrackerHTMiss","L1TrackerHTMiss", "MENUTREE") ),


   maxL1Extra = cms.uint32(50)
)

#### Gen level tree

from L1Trigger.L1TNtuples.l1GeneratorTree_cfi  import l1GeneratorTree
genTree=l1GeneratorTree.clone()

runmenutree=cms.Path(l1PhaseIITree*genTree)




