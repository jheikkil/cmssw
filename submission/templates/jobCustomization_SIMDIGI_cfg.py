import FWCore.ParameterSet.Config as cms

from input_cfg import process

process.maxEvents.input = cms.untracked.int32(TEMPL_NEVENTS)

process.source.fileNames = cms.untracked.vstring(TEMPL_INFILES)
process.RandomNumberGeneratorService.generator.initialSeed = cms.untracked.uint32(TEMPL_SEED)
process.RandomNumberGeneratorService.VtxSmeared.initialSeed = cms.untracked.uint32(TEMPL_SEED)
# process.source.firstLuminosityBlock = cms.untracked.uint32(TEMPL_SEED)
process.FEVTDEBUGHLToutput.fileName = cms.untracked.string('file:TEMPL_OUTFILE')

if hasattr(process.mix, 'input'):
    process.mix.input.fileNames = cms.untracked.vstring(TEMPL_PUFILELIST)
