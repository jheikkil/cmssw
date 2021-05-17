// -*- C++ -*-
//
// Package:    L1Trigger/Phase2L1GMT
// Class:      Phase2L1TGMTSAMuonProducer
//
/**\class Phase2L1TGMTSAMuonProducer Phase2L1TGMTSAMuonProducer.cc L1Trigger/Phase2L1GMT/plugins/Phase2L1TGMTSAMuonProducer.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Zhenbin Wu
//         Created:  Fri, 30 Apr 2021 19:10:59 GMT
//
//

#ifndef PHASE2GMT_SAMUONPRODUCER
#define PHASE2GMT_SAMUONPRODUCER

// system include files
#include <memory>
#include <sstream>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/stream/EDProducer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Utilities/interface/StreamID.h"

#include "DataFormats/L1Trigger/interface/Muon.h"
#include "DataFormats/L1Trigger/interface/L1MuonParticleFwd.h"
#include "DataFormats/L1Trigger/interface/L1MuonParticle.h"

#include "L1Trigger/Phase2L1GMT/interface/Constants.h"
#include "DataFormats/L1TMuonPhase2/interface/SAMuon.h"
//
// class declaration
//
using namespace Phase2L1GMT;
using namespace l1t;

class Phase2L1TGMTSAMuonProducer : public edm::stream::EDProducer<> {
public:
  explicit Phase2L1TGMTSAMuonProducer(const edm::ParameterSet&);
  ~Phase2L1TGMTSAMuonProducer() override;

  static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

private:
  void beginStream(edm::StreamID) override;
  void produce(edm::Event&, const edm::EventSetup&) override;
  void endStream() override;

  l1t::SAMuon Convertl1tMuon(const l1t::Muon& mu, const int bx_);

  // ----------member data ---------------------------
  edm::EDGetTokenT<BXVector<l1t::Muon> > muonToken_;
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
Phase2L1TGMTSAMuonProducer::Phase2L1TGMTSAMuonProducer(const edm::ParameterSet& iConfig)
    : muonToken_(consumes<l1t::MuonBxCollection>(iConfig.getUntrackedParameter<edm::InputTag>("muonToken"))) {
  produces<std::vector<l1t::SAMuon> >("promptSAMuons").setBranchAlias("prompt");
  produces<std::vector<l1t::SAMuon> >("displacedSAMuons").setBranchAlias("displaced");
}

Phase2L1TGMTSAMuonProducer::~Phase2L1TGMTSAMuonProducer() {}

//
// member functions
//

// ------------ method called to produce the data  ------------
void Phase2L1TGMTSAMuonProducer::produce(edm::Event& iEvent, const edm::EventSetup& iSetup) {
  using namespace edm;
  edm::Handle<l1t::MuonBxCollection> muon;
  iEvent.getByToken(muonToken_, muon);

  // Output
  const int Nprompt = 18;
  const int Ndisplaced = 18;
  std::vector<SAMuon> prompt;
  std::vector<SAMuon> displaced;

  for (int bx = muon->getFirstBX(); bx <= muon->getLastBX(); ++bx) {
    //TODO: We are expecting to send all BX. Using bx0 for now
    if (bx != 0) {
      continue;
    }

    for (uint i = 0; i < muon->size(bx); ++i) {
      const l1t::Muon& mu = muon->at(bx, i);

      //TODO: Still looking for a way to get displaced muon
      if (abs(mu.hwDXY()) > 0)
        displaced.push_back(Convertl1tMuon(mu, bx));
      else
        prompt.push_back(Convertl1tMuon(mu, bx));
    }

    // Sort by hwPt
    std::sort(prompt.begin(), prompt.end(), std::greater<>());
    std::sort(displaced.begin(), displaced.end(), std::greater<>());

    // Store into output, allow up to 18 prompt + 18 displayed
    if (prompt.size() > Nprompt) {
      prompt.resize(Nprompt);
    }
    if (displaced.size() > Ndisplaced) {
      displaced.resize(Ndisplaced);
    }
  }

  std::unique_ptr<std::vector<l1t::SAMuon> > prompt_ptr = std::make_unique<std::vector<l1t::SAMuon> >(prompt);
  std::unique_ptr<std::vector<l1t::SAMuon> > displaced_ptr = std::make_unique<std::vector<l1t::SAMuon> >(displaced);
  iEvent.put(std::move(prompt_ptr), "promptSAMuons");
  iEvent.put(std::move(displaced_ptr), "displacedSAMuons");
}

// ===  FUNCTION  ============================================================
//         Name:  Phase2L1TGMTSAMuonProducer::Convertl1tMuon
//  Description:
// ===========================================================================
SAMuon Phase2L1TGMTSAMuonProducer::Convertl1tMuon(const l1t::Muon& mu, const int bx_) {
  ap_uint<BITSQUALITY> qual = mu.hwQual();
  // We might not need to send BX info
  //ap_int<BITSBX> bx(bx_);
  bool charge(mu.charge() > 0);
  ap_uint<BITSPT> pt = round(mu.pt() / 0.025);
  ap_int<BITSPHI> phi = round(mu.phi() * (1 << (BITSPHI - 1)) / (M_PI));
  ap_int<BITSETA> eta = round(mu.eta() * (1 << (BITSETA - 1)) / (M_PI));
  // FIXME: Below are not well defined in phase1 GMT
  // Using the version from Correlator for now
  ap_int<BITSSAZ0> z0 = 0;  // No tracks info in Phase 1
  ap_int<BITSSAD0> d0 =
      mu.hwDXY();  // Use 2 bits with LSB = 30cm for BMTF and 25cm for EMTF currently, but subjet to change
  ap_uint<BITSSABETA> beta = 0;  // No beta from l1t::Muon

  ap_uint<64> word(0);
  word = word.concat(beta);
  word = word.concat(d0);
  word = word.concat(z0);
  word = word.concat(eta);
  word = word.concat(phi);
  word = word.concat(pt);
  word = word.concat(ap_uint<1>(charge));
  word = word.concat(qual);
  //word = word.concat(bx);

  SAMuon samuon(mu, charge, pt.to_uint(), eta.to_int(), phi.to_int(), z0.to_int(), d0.to_int(), qual.to_uint());
  samuon.setBeta(beta.to_uint());
  samuon.setWord(word);
  return samuon;
}  // -----  end of function Phase2L1TGMTSAMuonProducer::Convertl1tMuon  -----

// ------------ method called once each stream before processing any runs, lumis or events  ------------
void Phase2L1TGMTSAMuonProducer::beginStream(edm::StreamID) {
  // please remove this method if not needed
}

// ------------ method called once each stream after processing all runs, lumis and events  ------------
void Phase2L1TGMTSAMuonProducer::endStream() {
  // please remove this method if not needed
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void Phase2L1TGMTSAMuonProducer::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(Phase2L1TGMTSAMuonProducer);
#endif
