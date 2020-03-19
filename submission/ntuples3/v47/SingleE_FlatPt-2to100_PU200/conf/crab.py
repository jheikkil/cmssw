from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

# config.General.requestName = 'SingleGammaPt25Eta1p6_2p8_PU0'
# config.Data.inputDataset = '/SingleGammaPt25Eta1p6_2p8/PhaseIITDRFall17DR-noPUFEVT_93X_upgrade2023_realistic_v2-v1/GEN-SIM-DIGI-RAW'

config.General.requestName = 'SingleE_FlatPt-2to100_PU200'
config.Data.inputDataset = '/SingleE_FlatPt-2to100/PhaseIIMTDTDRAutumn18DR-PU200_103X_upgrade2023_realistic_v2-v1/FEVT'

config.General.workArea = 'ntuples3/v47/SingleE_FlatPt-2to100_PU200'
config.General.transferOutputs = True
config.General.transferLogs = False

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'ntuples3/v47/SingleE_FlatPt-2to100_PU200/conf/input_cfg.py'

config.Data.inputDBS = 'global'
config.Data.splitting = 'Automatic'
config.Data.unitsPerJob = 200
config.Data.totalUnits = -1
config.Data.outLFNDirBase = '/store/user/jheikkil/TRG3/'
config.Data.publication = False
config.Data.ignoreLocality = False
config.Data.outputDatasetTag = 'SingleE_FlatPt-2to100_PU200_v47'

config.Site.storageSite = 'T2_CH_CERN'
config.JobType.allowUndistributedCMSSW = True
