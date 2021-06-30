#include "L1Trigger/L1TTrackMatch/interface/L1TkEtMissEmuTrackTransform.h"

#include <cmath>

void L1TkEtMissEmuTrackTransform::generateLUTs() {
  phiQuadrants = generatePhiSliceLUT(l1tmetemu::kNQuadrants);
  phiShift = generatePhiSliceLUT(l1tmetemu::kNSector);
}

global_phi_t L1TkEtMissEmuTrackTransform::localToGlobalPhi(TTTrack_TrackWord::phi_t local_phi,
                                                           global_phi_t sector_shift) {
  int PhiMin = 0;
  int PhiMax = phiQuadrants.back();
  int phiMultiplier = TTTrack_TrackWord::TrackBitWidths::kPhiSize - l1tmetemu::kInternalPhiWidth;

  int tempPhi =
      floor(unpackSignedValue(local_phi, TTTrack_TrackWord::TrackBitWidths::kPhiSize) / pow(2, phiMultiplier)) +
      sector_shift;

  if (tempPhi < PhiMin) {
    tempPhi = tempPhi + PhiMax;
  } else if (tempPhi > PhiMax) {
    tempPhi = tempPhi - PhiMax;
  } else
    tempPhi = tempPhi;

  global_phi_t globalPhi = global_phi_t(tempPhi);

  return globalPhi;
}

nstub_t L1TkEtMissEmuTrackTransform::countNStub(TTTrack_TrackWord::hit_t Hitpattern) {
  nstub_t Nstub = 0;
  for (int i = (TTTrack_TrackWord::kHitPatternSize - 1); i >= 0; i--) {
    int k = Hitpattern >> i;
    if (k & 1)
      Nstub++;
  }
  return Nstub;
}

TTTrack_TrackWord::phi_t L1TkEtMissEmuTrackTransform::floatGlobalPhiToSectorPhi(float phi, unsigned int sector) {
  float tempPhi = 0.0;
  if (sector < 4) {
    tempPhi = phi - (sector * (2 * M_PI) / 9);
  } else if (sector > 5) {
    tempPhi = phi + ((9 - sector) * (2 * M_PI) / 9);
  } else if (sector == 4) {
    if (phi > 0) {
      tempPhi = phi - (sector * (2 * M_PI) / 9);
    } else {
      tempPhi = phi + ((9 - sector) * (2 * M_PI) / 9);
    }
  } else if (sector == 5) {
    if (phi < 0) {
      tempPhi = phi + ((9 - sector) * (2 * M_PI) / 9);
    } else {
      tempPhi = phi - (sector * (2 * M_PI) / 9);
    }
  }
  return digitizeSignedValue<TTTrack_TrackWord::phi_t>(
      tempPhi, TTTrack_TrackWord::TrackBitWidths::kPhiSize, TTTrack_TrackWord::stepPhi0);
}

std::vector<global_phi_t> L1TkEtMissEmuTrackTransform::generatePhiSliceLUT(unsigned int N) {
  float sliceCentre = 0.0;
  std::vector<global_phi_t> phiLUT;
  for (unsigned int q = 0; q <= N; q++) {
    phiLUT.push_back((global_phi_t)(sliceCentre / l1tmetemu::kStepPhi));
    sliceCentre += 2 * M_PI / N;
  }
  return phiLUT;
}
