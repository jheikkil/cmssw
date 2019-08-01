# HGCal L1-Trigger e/gamma ID
This repository contains a series of scripts which are used to train the e/gamma ID BDT for the HGCal L1T. The workflow has been separated into subfoleder (see below), which must be ran in the correct order. The output is two .xml files, which contain the info of the trained BDT in the low eta (1.5 < |eta| < 2.7) and high eta (2.7 < |eta| < 3.0) regions. These .xml files can then be placed directly in the HGCAL L1T TPG software.


## Installation
Follow the instructions for installation (users) of the [HGCAL L1T TPG software](https://twiki.cern.ch/twiki/bin/viewauth/CMS/HGCALTriggerPrimitivesSimulation#Installation_for_users)

The next step is to clone this repository:

```
cd L1Trigger
git clone git@github.com:jonathon-langford/hgcal_l1t_egid
```
In each new terminal, must set environment: `source setup.sh`

## Contents
Each subfolder contains instructions in the form of a `README.md` which details how to run the scripts:

* `ntuples`: contains the CMSSW config to create ntuples from the HGCAL L1T TPG software. The ntuple production uses CRAB and thus requires a grid certificate. 
* `cl3d_selection`: takes as input the ntuples produced in the `ntuples` subfolder and outputs a tree of 3d clusters passing the selection criteria for training the e/gamma ID.
* `training`: scripts for training the e/gamma ID BDT, converting into .xml format, evaluating the newly-trained BDTs and summaries the performance (working points,ROC curve)
* `plotting`: scripts to plot the efficiency curves and the 3D cluster variables.

For the full workflow users should: `ntuples` -> `cl3d_selection` -> `training`

