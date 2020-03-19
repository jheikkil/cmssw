from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

# config.General.requestName = 'SingleGammaPt25Eta1p6_2p8_PU0'
# config.Data.inputDataset = '/SingleGammaPt25Eta1p6_2p8/PhaseIITDRFall17DR-noPUFEVT_93X_upgrade2023_realistic_v2-v1/GEN-SIM-DIGI-RAW'

config.General.requestName = 'TEMPL_REQUESTNAME'
config.Data.inputDataset = 'TEMPL_INPUTDATASET'

# config.General.requestName = 'SingleElectronPt5_100Eta1p6_2p8_PU0_v0'
# config.Data.inputDataset = '/SingleElectronPt5_100Eta1p6_2p8/PhaseIITDRFall17DR-noPUFEVT_93X_upgrade2023_realistic_v2-v1/GEN-SIM-DIGI-RAW'


# config.General.requestName = 'SingleGammaPt50Eta1p6_2p8_PU0_v4'
# config.Data.inputDataset = '/SingleGammaPt50Eta1p6_2p8/PhaseIITDRFall17DR-noPUFEVT_93X_upgrade2023_realistic_v2-v1/GEN-SIM-DIGI-RAW'


# config.General.requestName = 'SingleGammaPt35Eta1p6_2p8_PU200_v4'
# config.Data.inputDataset = '/SingleGammaPt35Eta1p6_2p8/PhaseIITDRFall17DR-PU200FEVT_93X_upgrade2023_realistic_v2-v3/GEN-SIM-DIGI-RAW'


# config.General.requestName = 'SingleGammaPt50Eta1p6_2p8_PU200_v4'
# config.Data.inputDataset = '/SingleGammaPt50Eta1p6_2p8/PhaseIITDRFall17DR-PU200FEVT_93X_upgrade2023_realistic_v2-v1/GEN-SIM-DIGI-RAW'


config.General.workArea = 'TEMPL_TASKCONFDIR'
config.General.transferOutputs = True
config.General.transferLogs = False

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'conf/input_cfg.py'

config.Data.inputDBS = 'global'
config.Data.splitting = 'TEMPL_SPLITGRANULARITY'
config.Data.unitsPerJob = TEMPL_SPLITGRANULARITY
config.Data.totalUnits = TEMPL_NEVENTS
config.Data.outLFNDirBase = '/store/group/cmst3/group/l1tr/cerminar/hgcal/CMSSW1015/'
config.Data.publication = False
config.Data.ignoreLocality = False
#config.Data.outputDatasetTag = 'CRAB3_tutorial_May2015_MC_analysis'

config.Site.storageSite = 'T2_CH_CERN'
