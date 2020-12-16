#ifndef __L1Analysis_L1AnalysisPhaseIIStep1DataFormat_H__
#define __L1Analysis_L1AnalysisPhaseIIStep1DataFormat_H__

//-------------------------------------------------------------------------------
// Created 20/04/2010 - E. Conte, A.C. Le Bihan
//
//
// Original code : UserCode/L1TriggerDPG/L1ExtraTreeProducer - Jim Brooke
//-------------------------------------------------------------------------------

#include <vector>

namespace L1Analysis {
  struct L1AnalysisPhaseIIStep1DataFormat {
    L1AnalysisPhaseIIStep1DataFormat() { Reset(); };
    ~L1AnalysisPhaseIIStep1DataFormat(){};

    void Reset() {
      z0Puppi = 0;
      z0L1TkPV.clear();
      sumL1TkPV.clear();
      nL1TkPVs = 0;

      nCaloTaus = 0;
      caloTauEt.clear();
      caloTauEta.clear();
      caloTauPhi.clear();
      caloTauIEt.clear();
      caloTauIEta.clear();
      caloTauIPhi.clear();
      caloTauIso.clear();
      caloTauBx.clear();
      caloTauTowerIPhi.clear();
      caloTauTowerIEta.clear();
      caloTauRawEt.clear();
      caloTauIsoEt.clear();
      caloTauNTT.clear();
      caloTauHasEM.clear();
      caloTauIsMerged.clear();
      caloTauHwQual.clear();

      nPfPhase1L1Jets = 0;
      pfPhase1L1JetEt.clear();
      pfPhase1L1JetEta.clear();
      pfPhase1L1JetPhi.clear();

      pfPhase1L1HT.clear();
      pfPhase1L1MHTEt.clear();
      pfPhase1L1MHTPhi.clear();
      nPfPhase1L1MHT = 0;

      nEG = 0;
      EGEt.clear();
      EGEta.clear();
      EGPhi.clear();
      EGBx.clear();
      EGIso.clear();
      EGzVtx.clear();
      EGHwQual.clear();
      EGHGC.clear();
      EGPassesLooseTrackID.clear();
      EGPassesPhotonID.clear();

      nTkElectrons = 0;
      tkElectronEt.clear();
      tkElectronEta.clear();
      tkElectronPhi.clear();
      tkElectronChg.clear();
      tkElectronBx.clear();
      tkElectronTrkIso.clear();
      tkElectronzVtx.clear();
      tkElectronHwQual.clear();
      tkElectronEGRefPt.clear();
      tkElectronEGRefEta.clear();
      tkElectronEGRefPhi.clear();
      tkElectronHGC.clear();
      tkElectronPassesLooseTrackID.clear();
      tkElectronPassesPhotonID.clear();

      nTkPhotons = 0;
      tkPhotonEt.clear();
      tkPhotonEta.clear();
      tkPhotonPhi.clear();
      tkPhotonBx.clear();
      tkPhotonTrkIso.clear();
      tkPhotonTrkIsoPV.clear();
      tkPhotonzVtx.clear();
      tkPhotonHwQual.clear();
      tkPhotonEGRefPt.clear();
      tkPhotonEGRefEta.clear();
      tkPhotonEGRefPhi.clear();
      tkPhotonHGC.clear();
      tkPhotonPassesLooseTrackID.clear();
      tkPhotonPassesPhotonID.clear();


      nStandaloneMuons = 0;
      standaloneMuonPt.clear();
      standaloneMuonPt2.clear();
      standaloneMuonEta.clear();
      standaloneMuonPhi.clear();
      standaloneMuonChg.clear();
      standaloneMuonQual.clear();
      standaloneMuonBx.clear();
      standaloneMuonRegion.clear();
      standaloneMuonDXY.clear();


      nTkMuons = 0;
      tkMuonPt.clear();
      tkMuonEta.clear();
      tkMuonPhi.clear();
      tkMuonChg.clear();
      tkMuonTrkIso.clear();
      tkMuonBx.clear();
      tkMuonQual.clear();
      tkMuonzVtx.clear();
      tkMuonMuRefPt.clear();
      tkMuonMuRefPhi.clear();
      tkMuonMuRefEta.clear();
      tkMuonDRMuTrack.clear();
      tkMuonNMatchedTracks.clear();
      tkMuonMuRefChg.clear();
      tkMuonRegion.clear();


      //global
      nGlobalMuons = 0;
      globalMuonPt.clear();
      globalMuonEta.clear();
      globalMuonPhi.clear();
      globalMuonEtaAtVtx.clear();
      globalMuonPhiAtVtx.clear();
      globalMuonIEt.clear();
      globalMuonIEta.clear();
      globalMuonIPhi.clear();
      globalMuonIEtaAtVtx.clear();
      globalMuonIPhiAtVtx.clear();
      globalMuonIDEta.clear();
      globalMuonIDPhi.clear();
      globalMuonChg.clear();
      globalMuonIso.clear();
      globalMuonQual.clear();
      globalMuonTfMuonIdx.clear();
      globalMuonBx.clear();


      nTkGlbMuons = 0;
      tkGlbMuonPt.clear();
      tkGlbMuonEta.clear();
      tkGlbMuonPhi.clear();
      tkGlbMuonChg.clear();
      tkGlbMuonTrkIso.clear();
      tkGlbMuonBx.clear();
      tkGlbMuonQual.clear();
      tkGlbMuonzVtx.clear();
      tkGlbMuonMuRefPt.clear();
      tkGlbMuonTrkRefPt.clear();
      tkGlbMuonMuRefPhi.clear();
      tkGlbMuonMuRefEta.clear();
      tkGlbMuonDRMuTrack.clear();
      tkGlbMuonNMatchedTracks.clear();
 

      puppiMETEt = 0;
      puppiMETPhi = 0;

      nNNTaus = 0;
      nnTauEt.clear();
      nnTauEta.clear();
      nnTauPhi.clear();
      nnTauChg.clear();
      nnTauChargedIso.clear();
      nnTauFullIso.clear();
      nnTauID.clear();
      nnTauPassLooseNN.clear();
      nnTauPassLoosePF.clear();
      nnTauPassTightPF.clear();
      nnTauPassTightNN.clear();
   
      // TkJets
      nTrackerJets = 0;
      trackerJetEt.clear();
      trackerJetEta.clear();
      trackerJetPhi.clear();
      trackerJetBx.clear();
      trackerJetzVtx.clear();

      // TrackerMet
      nTrackerMet = 0;
      trackerMetSumEt.clear();
      trackerMetEt.clear();
      trackerMetPhi.clear();
      trackerMetBx.clear();

      //trackerMHT
      nTrackerMHT = 0;
      trackerHT.clear();
      trackerMHT.clear();
      trackerMHTPhi.clear();
    }

    double z0Puppi;
    unsigned short int nL1TkPVs;
    std::vector<double> z0L1TkPV;
    std::vector<double> sumL1TkPV;

    unsigned short int nCaloTaus;
    std::vector<double> caloTauEt;
    std::vector<double> caloTauEta;
    std::vector<double> caloTauPhi;
    std::vector<short int> caloTauIEt;
    std::vector<short int> caloTauIEta;
    std::vector<short int> caloTauIPhi;
    std::vector<short int> caloTauIso;
    std::vector<short int> caloTauBx;
    std::vector<short int> caloTauTowerIPhi;
    std::vector<short int> caloTauTowerIEta;
    std::vector<short int> caloTauRawEt;
    std::vector<short int> caloTauIsoEt;
    std::vector<short int> caloTauNTT;
    std::vector<short int> caloTauHasEM;
    std::vector<short int> caloTauIsMerged;
    std::vector<short int> caloTauHwQual;

    unsigned short int nPfPhase1L1Jets;
    std::vector<double> pfPhase1L1JetEt;
    std::vector<double> pfPhase1L1JetEta;
    std::vector<double> pfPhase1L1JetPhi;

    std::vector<double> pfPhase1L1HT;
    std::vector<double> pfPhase1L1MHTEt;
    std::vector<double> pfPhase1L1MHTPhi;
    unsigned int nPfPhase1L1MHT;

    unsigned int nEG;
    std::vector<double> EGEt;
    std::vector<double> EGEta;
    std::vector<double> EGPhi;
    std::vector<int> EGBx;
    std::vector<double> EGIso;
    std::vector<double> EGzVtx;
    std::vector<int> EGHwQual;
    std::vector<unsigned int> EGHGC;
    std::vector<unsigned int> EGPassesLooseTrackID;
    std::vector<unsigned int> EGPassesPhotonID;

    unsigned int nTkElectrons;
    std::vector<double> tkElectronEt;
    std::vector<double> tkElectronEta;
    std::vector<double> tkElectronPhi;
    std::vector<int> tkElectronChg;
    std::vector<int> tkElectronBx;
    std::vector<double> tkElectronTrkIso;
    std::vector<double> tkElectronzVtx;
    std::vector<double> tkElectronHwQual;
    std::vector<double> tkElectronEGRefPt;
    std::vector<double> tkElectronEGRefEta;
    std::vector<double> tkElectronEGRefPhi;
    std::vector<unsigned int> tkElectronHGC;
    std::vector<unsigned int> tkElectronPassesLooseTrackID;
    std::vector<unsigned int> tkElectronPassesPhotonID;

    unsigned int nTkPhotons;
    std::vector<double> tkPhotonEt;
    std::vector<double> tkPhotonEta;
    std::vector<double> tkPhotonPhi;
    std::vector<int> tkPhotonBx;
    std::vector<double> tkPhotonTrkIso;
    std::vector<double> tkPhotonTrkIsoPV;
    std::vector<double> tkPhotonzVtx;
    std::vector<double> tkPhotonHwQual;
    std::vector<double> tkPhotonEGRefPt;
    std::vector<double> tkPhotonEGRefEta;
    std::vector<double> tkPhotonEGRefPhi;
    std::vector<unsigned int> tkPhotonHGC;
    std::vector<unsigned int> tkPhotonPassesLooseTrackID;
    std::vector<unsigned int> tkPhotonPassesPhotonID;


    unsigned short int nStandaloneMuons;
    std::vector<double> standaloneMuonPt;
    std::vector<double> standaloneMuonPt2;
    std::vector<double> standaloneMuonEta;
    std::vector<double> standaloneMuonPhi;
    std::vector<short int> standaloneMuonChg;
    std::vector<unsigned short int> standaloneMuonQual;
    std::vector<double> standaloneMuonDXY;
    std::vector<short int> standaloneMuonBx;
    std::vector<unsigned int> standaloneMuonRegion;


    unsigned int nTkMuons;
    std::vector<double> tkMuonPt;
    std::vector<double> tkMuonEta;
    std::vector<double> tkMuonPhi;
    std::vector<int> tkMuonChg;
    std::vector<double> tkMuonTrkIso;
    std::vector<int> tkMuonBx;
    std::vector<unsigned int> tkMuonQual;
    std::vector<double> tkMuonzVtx;
    std::vector<double> tkMuonMuRefPt;
    std::vector<double> tkMuonMuRefPhi;
    std::vector<double> tkMuonMuRefEta;
    std::vector<double> tkMuonDRMuTrack;
    std::vector<double> tkMuonNMatchedTracks;
    std::vector<int> tkMuonMuRefChg;
    std::vector<unsigned int> tkMuonRegion;

    unsigned short int nGlobalMuons;
    std::vector<double> globalMuonPt;
    std::vector<double> globalMuonEta;
    std::vector<double> globalMuonPhi;
    std::vector<double> globalMuonEtaAtVtx;
    std::vector<double> globalMuonPhiAtVtx;
    std::vector<short int> globalMuonIEt;
    std::vector<short int> globalMuonIEta;
    std::vector<short int> globalMuonIPhi;
    std::vector<short int> globalMuonIEtaAtVtx;
    std::vector<short int> globalMuonIPhiAtVtx;
    std::vector<short int> globalMuonIDEta;
    std::vector<short int> globalMuonIDPhi;
    std::vector<short int> globalMuonChg;
    std::vector<unsigned short int> globalMuonIso;
    std::vector<unsigned short int> globalMuonQual;
    std::vector<unsigned short int> globalMuonTfMuonIdx;
    std::vector<short int> globalMuonBx;

    unsigned int nTkGlbMuons;
    std::vector<double> tkGlbMuonPt;
    std::vector<double> tkGlbMuonEta;
    std::vector<double> tkGlbMuonPhi;
    std::vector<int> tkGlbMuonChg;
    std::vector<unsigned int> tkGlbMuonIso;
    std::vector<double> tkGlbMuonTrkIso;
    std::vector<int> tkGlbMuonBx;
    std::vector<unsigned int> tkGlbMuonQual;
    std::vector<double> tkGlbMuonzVtx;
    std::vector<double> tkGlbMuonMuRefPt;
    std::vector<double> tkGlbMuonTrkRefPt;
    std::vector<double> tkGlbMuonMuRefPhi;
    std::vector<double> tkGlbMuonMuRefEta;
    std::vector<double> tkGlbMuonDRMuTrack;
    std::vector<double> tkGlbMuonNMatchedTracks;


    double puppiMETEt;
    double puppiMETPhi;

    unsigned int nNNTaus;
    std::vector<double> nnTauEt;
    std::vector<double> nnTauEta;
    std::vector<double> nnTauPhi;
    std::vector<int> nnTauChg;
    std::vector<double> nnTauChargedIso;
    std::vector<double> nnTauFullIso;
    std::vector<unsigned int> nnTauID;
    std::vector<unsigned int> nnTauPassLooseNN;
    std::vector<unsigned int> nnTauPassLoosePF;
    std::vector<unsigned int> nnTauPassTightPF;
    std::vector<unsigned int> nnTauPassTightNN;

    unsigned int nTrackerJets;
    std::vector<double> trackerJetEt;
    std::vector<double> trackerJetEta;
    std::vector<double> trackerJetPhi;
    std::vector<int> trackerJetBx;
    std::vector<double> trackerJetzVtx;

    unsigned int nTrackerMet;
    std::vector<double> trackerMetSumEt;
    std::vector<double> trackerMetEt;
    std::vector<double> trackerMetPhi;
    std::vector<double> trackerMetBx;

    unsigned int nTrackerMHT;
    std::vector<double> trackerHT;
    std::vector<double> trackerMHT;
    std::vector<double> trackerMHTPhi;
  };
}  // namespace L1Analysis
#endif
