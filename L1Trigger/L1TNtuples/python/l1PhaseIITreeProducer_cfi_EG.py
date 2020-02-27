import FWCore.ParameterSet.Config as cms

l1PhaseIITree = cms.EDAnalyzer("L1PhaseIITreeProducer",

   egTokenBarrel = cms.InputTag("L1EGammaClusterEmuProducer","L1EGammaCollectionBXVEmulator"),
   tkEGTokenBarrel = cms.InputTag("L1TkElectronsCrystal","EG"),
   tkEGV2TokenBarrel = cms.InputTag("L1TkElectronsEllipticMatchCrystal","EG"),
   tkEMTokenBarrel = cms.InputTag("L1TkPhotonsCrystal","EG"),

   egTokenHGC = cms.InputTag("l1EGammaEEProducer","L1EGammaCollectionBXVWithCuts"),
   tkEGTokenHGC = cms.InputTag("L1TkElectronsHGC","EG"),
   tkEGV2TokenHGC = cms.InputTag("L1TkElectronsEllipticMatchHGC","EG"),
   tkEMTokenHGC = cms.InputTag("L1TkPhotonsHGC","EG"),


   zoPuppi = cms.InputTag("l1pfProducerBarrel","z0"),
   l1vertextdr = cms.InputTag("VertexProducer","l1vertextdr"),
   l1vertices = cms.InputTag("VertexProducer","l1vertices"),
   l1TkPrimaryVertex= cms.InputTag("L1TkPrimaryVertex",""),


   maxL1Extra = cms.uint32(50)
)

#### Gen level tree

from L1Trigger.L1TNtuples.l1GeneratorTree_cfi  import l1GeneratorTree
genTree=l1GeneratorTree.clone()

runmenutree=cms.Path(l1PhaseIITree*genTree)




