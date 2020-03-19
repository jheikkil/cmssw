import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process('REPR',eras.Phase2C4_trigger)
#process = cms.Process('REPR',eras.Phase2C4_timing_layer_bar)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.Geometry.GeometryExtended2023D35Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2023D35_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(100)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
'/store/mc/PhaseIIMTDTDRAutumn18DR/SingleE_FlatPt-2to100/FEVT/PU200_103X_upgrade2023_realistic_v2-v1/70000/FF17CBE6-81E5-8D43-B58B-6DF17222820E.root',
),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('repr nevts:2'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.FEVTDEBUGHLToutput = cms.OutputModule("PoolOutputModule",
#    dataset = cms.untracked.PSet(
#        dataTier = cms.untracked.string('GEN-SIM-DIGI-RAW'),
#        filterName = cms.untracked.string('')
#    ),
    fileName = cms.untracked.string('file:step2_2ev_reprocess_slim.root'),
#    outputCommands = process.FEVTDEBUGHLTEventContent.outputCommands,
 outputCommands = cms.untracked.vstring('drop *', 'keep *_*_*_REPR'),
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition


# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, '103X_upgrade2023_realistic_v2', '')
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic', '')

process.GlobalTag = GlobalTag(process.GlobalTag, '103X_upgrade2023_realistic_v2', '') 

process.load('SimCalorimetry.HcalTrigPrimProducers.hcaltpdigi_cff')
process.load('CalibCalorimetry.CaloTPG.CaloTPGTranscoder_cfi')

# Path and EndPath definitions
process.L1simulation_step = cms.Path(process.SimL1Emulator)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.FEVTDEBUGHLToutput_step = cms.EndPath(process.FEVTDEBUGHLToutput)

process.load("L1Trigger.L1TNtuples.l1PhaseIITreeProducer_cfi")


process.TFileService = cms.Service("TFileService",
    fileName = cms.string('L1NtuplePhaseII_MTD.root')
)


for seq in [process.simTwinMuxDigis,
            process.rpcRecHits,
            # process.L1EGammaClusterEmuProducer,
            #process.l1KBmtfStubMatchedMuons,
            process.l1TkMuonStubEndCap,
            process.l1TkMuonStubEndCapS12,
            # process.L1TkElectronsCrystal,
            process.L1TkMuons,
            process.L1TkMuonsTP,
            process.L1TkGlbMuons,
            #process.pfClustersFromL1EGClusters,
            #process.pfClustersFromCombinedCaloHCal,
            #process.pfClustersFromCombinedCaloHF,
            #process.pfClustersFromHGC3DClusters,
            #process.pfTracksFromL1TracksBarrel,
            #process.l1pfProducerBarrel,
            #process.pfTracksFromL1TracksHGCal,
            #process.l1pfProducerHGCal,
            #process.l1pfProducerHF,
            #process.l1pfCandidates,
            process.ak4PFL1Calo,
            process.ak4PFL1PF,
            process.ak4PFL1Puppi,
            process.ak4PFL1CaloCorrected,
            process.ak4PFL1PFCorrected,
            process.ak4PFL1PuppiCorrected,
            process.l1PFMetCalo,
            process.l1PFMetPF,
            process.l1PFMetPuppi,
            process.l1pfTauProducer,
            process.l1NNTauProducer,
            process.l1NNTauProducerPuppi,
            process.l1TkBsCandidates,
            process.l1TkBsCandidatesLooseWP,
            process.l1TkBsCandidatesTightWP,
            process.simCaloStage2Layer1Digis,
            process.simCaloStage2Digis,
            process.simDtTriggerPrimitiveDigis,
            process.simCscTriggerPrimitiveDigis,
            process.simBmtfDigis,
            process.simKBmtfStubs,
            process.simKBmtfDigis,
            process.simMuonME0PseudoReDigisCoarse,
            process.me0RecHitsCoarse,
            process.me0TriggerPseudoDigis,
            process.simEmtfDigis,
            process.simOmtfDigis,
            process.simGmtCaloSumDigis,
            process.simGmtStage2Digis,
            process.simGtExtFakeStage2Digis,
            process.simGtStage2Digis,
            process.me0RecHits,
            process.me0Segments,
            # process.me0TriggerPseudoDigis105X,
            process.simEcalEBTriggerPrimitiveDigis,
            # process.l1TkMuonStubOverlap,
            #process.l1pfProducerHGCalNoTK,
            #process.l1pfPhase1L1TJetProducer,
            # process.L1TkElectronsEllipticMatchCrystal,
            process.L1TkIsoElectronsHGC,
            process.L1TkElectronsLooseHGC,
]:
    if not process.L1simulation_step.remove(seq):
        print 'Failed to remove sequence: {}'.format(seq)


# Schedule definition
process.schedule = cms.Schedule(process.L1simulation_step,#process.extraCollectionsMenuTree,
            process.runmenutree,process.endjob_step)#,process.FEVTDEBUGHLToutput_step)

# Schedule definition
#process.schedule = cms.Schedule(process.L1simulation_step,process.endjob_step,process.FEVTDEBUGHLToutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)


# Customisation from command line

from L1Trigger.Configuration.customiseUtils import L1TrackTriggerTracklet
process = L1TrackTriggerTracklet(process)

process.MessageLogger.cout = cms.untracked.PSet(
    threshold = cms.untracked.string('ERROR'),
    default = cms.untracked.PSet(
        limit = cms.untracked.int32(10000)
    )
)

#from L1Trigger.L1TMuonEndCap.customise_Phase2 import customise as customise_Phase2
#process = customise_Phase2(process)


# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion

