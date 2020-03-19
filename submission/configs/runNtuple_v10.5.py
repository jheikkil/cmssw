# Auto generated configuration file
# using:
# Revision: 1.19
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v
# with command line options: repr --processName=REPR --python_filename=reprocess_test_10_5_0_pre1.py --no_exec -s L1 --datatier GEN-SIM-DIGI-RAW -n 2 --era Phase2 --eventcontent FEVTDEBUGHLT --filein root://cms-xrd-global.cern.ch//store/mc/PhaseIIMTDTDRAutumn18DR/DYToLL_M-50_14TeV_pythia8/FEVT/PU200_pilot_103X_upgrade2023_realistic_v2_ext4-v1/280000/FF5C31D5-D96E-5E48-B97F-61A0E00DF5C4.root --conditions 103X_upgrade2023_realistic_v2 --beamspot HLLHC14TeV --geometry Extended2023D28 --fileout file:step2_2ev_reprocess_slim.root
import FWCore.ParameterSet.Config as cms

from Configuration.ProcessModifiers.convertHGCalDigisSim_cff import convertHGCalDigisSim
from Configuration.StandardSequences.Eras import eras

process = cms.Process('REPR',eras.Phase2_trigger,convertHGCalDigisSim)
#process = cms.Process('REPR',eras.Phase2C4_timing_layer_bar)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.Geometry.GeometryExtended2023D17Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2023D17_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')


process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(10)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('/store/relval/CMSSW_9_3_7/RelValTTbar_14TeV/GEN-SIM-DIGI-RAW/PU25ns_93X_upgrade2023_realistic_v5_2023D17PU200-v1/10000/0A52EE7F-1E2D-E811-86EB-0242AC130002.root'),
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
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('GEN-SIM-DIGI-RAW'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('file:step2_2ev_reprocess_slim.root'),
    outputCommands = process.FEVTDEBUGHLTEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

# Additional output definition
process.TFileService = cms.Service(
    "TFileService",
    fileName = cms.string("ntuple.root")
    )


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
# process.FEVTDEBUGHLToutput_step = cms.EndPath(process.FEVTDEBUGHLToutput)



from L1Trigger.L1THGCalUtilities.hgcalTriggerChains import HGCalTriggerChains
import L1Trigger.L1THGCalUtilities.vfe as vfe
import L1Trigger.L1THGCalUtilities.concentrator as concentrator
import L1Trigger.L1THGCalUtilities.clustering2d as clustering2d
import L1Trigger.L1THGCalUtilities.clustering3d as clustering3d


chain = HGCalTriggerChains()
chain.register_vfe("VFEfp7", vfe.create_compression)
chain.register_concentrator("tcTh", concentrator.create_threshold)
chain.register_concentrator("sTC", concentrator.create_supertriggercell)

chain.register_backend1("dRNNC2d", clustering2d.create_constrainedtopological)
chain.register_backend1("dummyC2d", clustering2d.create_dummy)

chain.register_backend2("histoMaxC3dVR", clustering3d.create_histoMax_variableDr)
chain.register_backend2("histoMaxC3dVRPhiBins", lambda p, i: clustering3d.create_histoMax_variableDr(p, i, nBins_Phi=108))

chain.register_backend2("dRC3d", clustering3d.create_distance)


# chain.register_chain('VFEfp7', 'tcTh', 'dummyC2d', 'histoMaxC3d')
chain.register_chain('VFEfp7', 'tcTh', 'dummyC2d', 'histoMaxC3dVR')
chain.register_chain('VFEfp7', 'tcTh', 'dummyC2d', 'histoMaxC3dVRPhiBins')
chain.register_chain('VFEfp7', 'sTC', 'dummyC2d', 'histoMaxC3dVR')
chain.register_chain('VFEfp7', 'tcTh', 'dRNNC2d', 'dRC3d')


# chain.register_chain('Floatingpoint7', 'Threshold', 'Dummy', 'Histothreshold')
# chain.register_chain('Floatingpoint7', 'Bestchoice', 'Dummy', 'Histothreshold')
process = chain.create_sequences(process)


process.load("L1Trigger.L1THGCalUtilities.caloTruthCells_cff")
process.caloTruthCellsProducer.triggerCells = cms.InputTag('VFEfp7:HGCalVFEProcessorSums')
process.caloTruth_step = cms.Path(process.caloTruthCells)

process.hgcalTowerMapProducer.InputTriggerCells = cms.InputTag('VFEfp7:HGCalVFEProcessorSums')
# process.hgcalTriggerPrimitives.remove(process.hgcalTowerMap)
# process.hgcalTriggerPrimitives.remove(process.hgcalTower)

# FIX some inputtags depending on the new sewquences
process.l1EGammaEEProducer.Multiclusters = cms.InputTag('VFEfp7tcThdummyC2dhistoMaxC3dVR:HGCalBackendLayer2Processor3DClustering')
process.pfClustersFromHGC3DClusters.src = cms.InputTag('VFEfp7tcThdummyC2dhistoMaxC3dVR:HGCalBackendLayer2Processor3DClustering')
# process.pfClustersFromHGC3DClustersEM.src = cms.InputTag('VFEfp7tcThdRNNC2ddRC3d:HGCalBackendLayer2Processor3DClustering')
process.L1TkElectronsHGC.L1EGammaInputTag = cms.InputTag('l1EGammaEEProducer:L1EGammaCollectionBXVWithCuts')
process.L1TkElectronsHGC.debug = cms.untracked.bool(False)

# customize Iso cuts a la suchandra
process.L1TkIsoElectronsHGC.L1EGammaInputTag = cms.InputTag('l1EGammaEEProducer:L1EGammaCollectionBXVWithCuts')
process.L1TkIsoElectronsHGC.DRmax = cms.double(0.4)
process.L1TkIsoElectronsHGC.DeltaZ = cms.double(1.0)
process.L1TkIsoElectronsHGC.maxChi2IsoTracks = cms.untracked.double(100)
process.L1TkIsoElectronsHGC.minNStubsIsoTracks = cms.untracked.int32(4)
process.L1TkIsoElectronsHGC.debug = cms.untracked.bool(False)

# load ntuplizer
process.load('L1Trigger.L1THGCalUtilities.hgcalTriggerNtuples_cff')
process.ntuple_step = cms.Path(process.hgcalTriggerNtuples)
process.hgcalTriggerNtuplizer.Ntuples.remove(process.ntuple_genjet)
process.hgcalTriggerNtuplizer.Ntuples.remove(process.ntuple_gentau)
process.hgcalTriggerNtuplizer.Ntuples.remove(process.ntuple_digis)
process.hgcalTriggerNtuplizer.Ntuples.remove(process.ntuple_triggercells)
process.hgcalTriggerNtuplizer.Ntuples.remove(process.ntuple_multiclusters)
process.hgcalTriggerNtuplizer.Ntuples.remove(process.ntuple_towers)



from L1Trigger.L1THGCal.egammaIdentification import egamma_identification_drnn_cone, \
                                                    egamma_identification_drnn_dbscan, \
                                                    egamma_identification_histomax

from L1Trigger.L1THGCalUtilities.hgcalTriggerNtuples_cfi import ntuple_triggercells
tc_ntp = ntuple_triggercells.clone()
tc_ntp.TriggerCells = cms.InputTag('VFEfp7tcTh:HGCalConcentratorProcessorSelection')
tc_ntp.Multiclusters = cms.InputTag('VFEfp7tcThdRNNC2ddRC3d:HGCalBackendLayer2Processor3DClustering')
process.hgcalTriggerNtuplizer.Ntuples.append(tc_ntp)

from L1Trigger.L1THGCalUtilities.hgcalTriggerNtuples_cfi import ntuple_clusters
cl2d_ntp = ntuple_clusters.clone()
cl2d_ntp.Clusters = cms.InputTag('VFEfp7tcThdRNNC2d:HGCalBackendLayer1Processor2DClustering')
cl2d_ntp.Multiclusters = cms.InputTag('VFEfp7tcThdRNNC2ddRC3d:HGCalBackendLayer2Processor3DClustering')
process.hgcalTriggerNtuplizer.Ntuples.append(cl2d_ntp)

from L1Trigger.L1THGCalUtilities.hgcalTriggerNtuples_cfi import ntuple_multiclusters
cl3d_ntp = ntuple_multiclusters.clone()
cl3d_ntp.Multiclusters = cms.InputTag('VFEfp7tcThdRNNC2ddRC3d:HGCalBackendLayer2Processor3DClustering')
cl3d_ntp.BranchNamePrefix = cms.untracked.string('cl3d')
cl3d_ntp.EGIdentification = egamma_identification_drnn_cone.clone()
process.hgcalTriggerNtuplizer.Ntuples.append(cl3d_ntp)
# cl3d_ntp1 = ntuple_multicluster.clone()
# cl3d_ntp1.Multiclusters = cms.InputTag('VFEfp7tcThdummyC2dhistoMaxC3d:HGCalBackendLayer2Processor3DClustering')
# cl3d_ntp1.BranchNamePrefix = cms.untracked.string('hmcl3d')
# process.hgcalTriggerNtuplizer.Ntuples.append(cl3d_ntp1)

cl3d_ntp2 = ntuple_multiclusters.clone()
cl3d_ntp2.Multiclusters = cms.InputTag('VFEfp7tcThdummyC2dhistoMaxC3dVR:HGCalBackendLayer2Processor3DClustering')
cl3d_ntp2.BranchNamePrefix = cms.untracked.string('hmVRcl3d')
process.hgcalTriggerNtuplizer.Ntuples.append(cl3d_ntp2)

cl3d_ntp3 = ntuple_multiclusters.clone()
cl3d_ntp3.Multiclusters = cms.InputTag('VFEfp7tcThdummyC2dhistoMaxC3dVRPhiBins:HGCalBackendLayer2Processor3DClustering')
cl3d_ntp3.BranchNamePrefix = cms.untracked.string('hmVRcl3dRebin')
process.hgcalTriggerNtuplizer.Ntuples.append(cl3d_ntp3)

cl3d_ntp4 = ntuple_multiclusters.clone()
cl3d_ntp4.Multiclusters = cms.InputTag('VFEfp7sTCdummyC2dhistoMaxC3dVR:HGCalBackendLayer2Processor3DClustering')
cl3d_ntp4.BranchNamePrefix = cms.untracked.string('hmVRcl3dSTC')
process.hgcalTriggerNtuplizer.Ntuples.append(cl3d_ntp4)

# cl3d_ntp5 = ntuple_multiclusters.clone()
# cl3d_ntp5.Multiclusters = cms.InputTag('VFEfp7tcThNCdummyC2dhistoMaxC3dVRNC:HGCalBackendLayer2Processor3DClustering')
# cl3d_ntp5.BranchNamePrefix = cms.untracked.string('hmVRcl3dNC1')
# process.hgcalTriggerNtuplizer.Ntuples.append(cl3d_ntp5)


from L1Trigger.L1CaloTrigger.ntuple_cfi import ntuple_egammaEE, ntuple_TTTracks, ntuple_tkEle
ntuple_tkEleHGC = ntuple_tkEle.clone()
ntuple_tkEleHGC.TkElectrons = cms.InputTag("L1TkElectronsHGC","EG")
ntuple_tkEleHGC.BranchNamePrefix = cms.untracked.string("tkEle")


ntuple_tkIsoEleHGC = ntuple_tkEle.clone()
ntuple_tkIsoEleHGC.TkElectrons = cms.InputTag("L1TkIsoElectronsHGC","EG")
ntuple_tkIsoEleHGC.BranchNamePrefix = cms.untracked.string("tkIsoEle")

process.hgcalTriggerNtuplizer.Ntuples.append(ntuple_egammaEE)
process.hgcalTriggerNtuplizer.Ntuples.append(ntuple_TTTracks)
process.hgcalTriggerNtuplizer.Ntuples.append(ntuple_tkEleHGC)
process.hgcalTriggerNtuplizer.Ntuples.append(ntuple_tkIsoEleHGC)


# Schedule definition
process.schedule = cms.Schedule(process.L1simulation_step, process.caloTruth_step, process.ntuple_step, process.endjob_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)


# Customisation from command line

# Automatic addition of the customisation function from L1Trigger.Configuration.customiseUtils
from L1Trigger.Configuration.customiseUtils import DropDepricatedProducts,L1TrackTriggerTracklet,DropOutputProducts

#call to customisation function DropDepricatedProducts imported from L1Trigger.Configuration.customiseUtils
process = DropDepricatedProducts(process)

from L1Trigger.Configuration.customiseUtils import L1TrackTriggerTracklet
process = L1TrackTriggerTracklet(process)

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
