import FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras

process = cms.Process("RESP", eras.Phase2C9)

process.load('Configuration.StandardSequences.Services_cff')
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True), allowUnscheduled = cms.untracked.bool(False) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000))
process.MessageLogger.cerr.FwkReport.reportEvery = 1

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring('file:inputs110X.root'),
    inputCommands = cms.untracked.vstring("keep *", 
            "drop l1tPFClusters_*_*_*",
            "drop l1tPFTracks_*_*_*",
            "drop l1tPFCandidates_*_*_*")
)

process.load('Configuration.Geometry.GeometryExtended2026D49Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2026D49_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('SimCalorimetry.HcalTrigPrimProducers.hcaltpdigi_cff') # needed to read HCal TPs
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '111X_mcRun4_realistic_Candidate_2020_12_09_15_46_46', '')

process.load("L1Trigger.Phase2L1ParticleFlow.l1ParticleFlow_cff")
process.load('L1Trigger.Phase2L1ParticleFlow.l1ctLayer1_cff')


doPVEmu = True

if doPVEmu:
    process.load('L1Trigger.L1TTrackMatch.L1GTTInputProducer_cfi')
    process.load('L1Trigger.VertexFinder.VertexProducer_cff')
    process.VertexProducer.l1TracksInputTag = cms.InputTag("L1GTTInputProducer", "Level1TTTracksConverted")
    process.VertexProducer.VertexReconstruction.Algorithm = cms.string("FastHistoEmulation")
    
    for l1ctbrd in [process.l1ctLayer1Barrel,
                    process.l1ctLayer1HGCal,
                    process.l1ctLayer1HGCalNoTK,
                    process.l1ctLayer1HF]:
        l1ctbrd.vtxCollection = cms.InputTag("VertexProducer", "l1verticesEmulation")
        l1ctbrd.vtxCollectionEmulation = True
        

    process.runPF = cms.Path( 
        process.L1GTTInputProducer +
        process.VertexProducer +
        process.pfTracksFromL1Tracks +
        process.l1ParticleFlow_calo +
        process.l1ctLayer1Barrel +
        process.l1ctLayer1HGCal +
        process.l1ctLayer1HGCalNoTK +
        process.l1ctLayer1HF +
        process.l1ctLayer1
    )
    
else:
    # FIXME: this is not working....might need to reproduce the input with the additional collections

    # process.load("L1Trigger.TrackFindingTracklet.L1HybridEmulationTracks_cff")
    process.load('L1Trigger.L1TTrackMatch.L1GTTInputProducer_cfi')
    process.load('L1Trigger.VertexFinder.VertexProducer_cff')

    process.L1VertexFinder = process.VertexProducer.clone()

    process.runPF = cms.Path( 
        # process.L1HybridTracks +
        # process.L1GTTInputProducer +
        # process.L1VertexFinder +
        process.pfTracksFromL1Tracks +
        process.l1ParticleFlow_calo +
        process.l1ctLayer1Barrel +
        process.l1ctLayer1HGCal +
        process.l1ctLayer1HGCalNoTK +
        process.l1ctLayer1HF +
        process.l1ctLayer1
    )

process.source.fileNames  = [ '/store/cmst3/group/l1tr/gpetrucc/11_1_0/NewInputs110X/110121.done/TTbar_PU200/inputs110X_%d.root' % i for i in (1,3,7,8,9) ]

for det in "Barrel", "HGCal", "HGCalNoTK", "HF":
    l1pf = getattr(process, 'l1ctLayer1'+det)
    l1pf.dumpFileName = cms.untracked.string("TTbar_PU200_"+det+".dump")
