from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config, getUsernameFromSiteDB

config = Configuration()

config.section_("General")
#config.General.requestName = 'WLNu_200PU_V7_1'
#config.General.requestName = 'HGG_200PU_V10_2'
#config.General.requestName = 'TT_200PU_V10_3'
#config.General.requestName = 'NeutrinoGun_10GeV_140_200PU_V10_3'
#config.General.requestName = 'GluGluHTauTau_V10_1'
#config.General.requestName = 'BsPhiPhi_V8_2'
config.General.requestName = 'DYLL_200PU_V10_1'
#config.General.requestName = 'BsToMuMu_V7_5_2'
#config.General.requestName = 'QCD_15To7000_V10_3'
#config.General.requestName = 'HH4B_V10_3'
#config.General.requestName = 'BdToKstarMuMu_V7_5_2'
#config.General.requestName = 'VBFHToBB_V10_3'

config.General.workArea = 'crab_tasksASOv2/'

config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'rerun_PhaseIITreeProducer_MenuTree_MTD.py'
# Uncomment the following line when running on PAT events
config.JobType.outputFiles = ['L1NtuplePhaseII_MTD.root']

config.section_("Data")
#config.Data.inputDataset ='/BsToPhiPhi_SoftQCDnonD_TuneCP5_14TeV_Pythia8/PhaseIIMTDTDRAutumn18DR-PU200_103X_upgrade2023_realistic_v2-v2/FEVT'
#config.Data.inputDataset ='/GluGluHToGG_M125_14TeV_powheg_pythia8/PhaseIIMTDTDRAutumn18DR-PU200_103X_upgrade2023_realistic_v2-v1/FEVT'
#config.Data.inputDataset ='/NeutrinoGun_E_10GeV/PhaseIIMTDTDRAutumn18DR-PU200_103X_upgrade2023_realistic_v2-v1/FEVT'
#config.Data.inputDataset ='/WToLNu_14TeV_TuneCP5_pythia8/PhaseIIMTDTDRAutumn18DR-PU200_103X_upgrade2023_realistic_v2-v1/FEVT'
config.Data.inputDataset ='/DYToLL_M-50_14TeV_TuneCP5_pythia8/PhaseIIMTDTDRAutumn18DR-PU200_103X_upgrade2023_realistic_v2-v2/FEVT'
#config.Data.inputDataset ='/TTbar_14TeV_TuneCP5_Pythia8/PhaseIIMTDTDRAutumn18DR-PU200_103X_upgrade2023_realistic_v2-v1/FEVT'
#config.Data.inputDataset ='/GluGluHToTauTau_M125_14TeV_powheg_pythia8/PhaseIIMTDTDRAutumn18DR-PU200_103X_upgrade2023_realistic_v2-v1/FEVT'
#config.Data.inputDataset ='/BsToMuMu_SoftQCDnonD_TuneCP5_14TeV-pythia8-evtgen/PhaseIIMTDTDRAutumn18DR-PU200_103X_upgrade2023_realistic_v2-v1/FEVT'
#config.Data.inputDataset ='/QCD_Pt-15To7000_TuneCP5_Flat_14TeV-pythia8/PhaseIIMTDTDRAutumn18DR-PU200_103X_upgrade2023_realistic_v2-v1/FEVT'
###config.Data.inputDataset ='/GluGluToHHTo4B_node_SM_14TeV-madgraph/PhaseIIMTDTDRAutumn18DR-PU200_103X_upgrade2023_realistic_v2-v1/FEVT'
#config.Data.inputDataset ='/BdToKstarMuMu_BMuonFilter_SoftQCDnonD_TuneCP5_14TeV-pythia8-evtgen/PhaseIIMTDTDRAutumn18DR-PU200_103X_upgrade2023_realistic_v2-v1/FEVT'
#config.Data.inputDataset ='/VBFHToBB_M-125_14TeV_powheg_pythia8_weightfix/PhaseIIMTDTDRAutumn18DR-PU200_103X_upgrade2023_realistic_v2-v1/FEVT'


#config.Data.allowNonValidInputDataset = True

config.Data.inputDBS = 'global'
#config.Data.splitting = 'Automatic'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 5

# Uncomment to run on a fraction of the dataset
#config.Data.outLFNDirBase = '/store/group/cmst3/user/cepeda/trigger' 

config.Data.outLFNDirBase = '/eos/cms/store/user/jheikkil/TRG/'
config.Data.publication = False

config.JobType.maxMemoryMB = 2500

config.JobType.allowUndistributedCMSSW = True 

#config.section_("Debug")
#config.Debug.extraJDL = ['+CMS_ALLOW_OVERFLOW=False']
#config.Debug.scheddName = 'crab3@vocms0198.cern.ch'

config.section_("Site")
config.Site.storageSite = 'T2_CH_CERN'
#config.Site.ignoreGlobalBlacklist = True
#config.Site.whitelist = 'T2_US_UW'
