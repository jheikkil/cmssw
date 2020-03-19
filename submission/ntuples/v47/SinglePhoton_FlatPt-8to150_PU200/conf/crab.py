from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

# config.General.requestName = 'SingleGammaPt25Eta1p6_2p8_PU0'
# config.Data.inputDataset = '/SingleGammaPt25Eta1p6_2p8/PhaseIITDRFall17DR-noPUFEVT_93X_upgrade2023_realistic_v2-v1/GEN-SIM-DIGI-RAW'

config.General.requestName = 'SinglePhoton_FlatPt-8to150_PU200'
config.Data.inputDataset = '/SinglePhoton_FlatPt-8to150/PhaseIIMTDTDRAutumn18DR-PU200_103X_upgrade2023_realistic_v2-v1/FEVT'

config.General.workArea = 'ntuples/v47/SinglePhoton_FlatPt-8to150_PU200'
config.General.transferOutputs = True
config.General.transferLogs = False

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'ntuples/v47/SinglePhoton_FlatPt-8to150_PU200/conf/input_cfg.py'

config.Data.inputDBS = 'global'
config.Data.splitting = 'Automatic'
config.Data.unitsPerJob = 200
config.Data.totalUnits = 200000
config.Data.outLFNDirBase = '/store/user/jheikkil/TRG/'
config.Data.publication = False
config.Data.ignoreLocality = False
config.Data.outputDatasetTag = 'SinglePhoton_FlatPt-8to150_PU200_v47'

config.JobType.maxMemoryMB = 2500

config.Site.storageSite = 'T2_CH_CERN'
config.JobType.allowUndistributedCMSSW = True
