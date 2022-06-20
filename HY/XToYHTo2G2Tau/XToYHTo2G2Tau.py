import pandas as pd
import numpy as np
import requests
import re
import csv
import copy
from os import path

def GetGridpacksAndDataset(gp, t_datasetname, res, mX, mY, verbose):
    gridpacks = copy.deepcopy(gp)
    gridpacks = gridpacks.replace("<massX>",str(mX)).replace("<massY>", str(mY))
    ### Check if gridpacks exist            
    gr_exists = path.exists(gridpacks)
    if (not gr_exists):
        print("[%s] Path %s does not exist!" % (res, gridpacks))
        gridpacks = None
    dataset_name = copy.deepcopy(t_datasetname)
    dataset_name = dataset_name.replace("<massX>",str(mX)).replace("<massY>", str(mY))
    
    note = dataset_name.replace('_',' ')

    if verbose: print("=== [%s, mX = %s, mY = %s] Dataset name: %s" % (res, mX, mY, dataset_name))
        
    return gridpacks, dataset_name, note

def GetFragments(LHEproducer, pythia_fragment_CP5, gridpacks, verbose):
    t_LHEproducer = copy.deepcopy(LHEproducer)
    final_fragment = t_LHEproducer.replace('__GRIDPACK__',gridpacks) + '\n' + pythia_fragment_CP5
    if verbose: print("=== final fragment: \n %s" % (final_fragment))
    return final_fragment
    

# fragments
pythia_fragment_CP5 = {}
# https://github.com/cms-sw/genproductions/blob/master/genfragments/ThirteenTeV/Higgs/HY/ResonanceDecayFilter_example_HY_XToYH_HTo2T_YTo2G.py
# https://github.com/cms-sw/genproductions/blob/master/genfragments/ThirteenTeV/Higgs/HY/ResonanceDecayFilter_example_HY_XToYH_HTo2G_YTo2T.py
pythia_fragment_CP5['Ygg_Htt'] = """
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *

generator = cms.EDFilter("Pythia8ConcurrentHadronizerFilter",
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13000.),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        pythia8PSweightsSettingsBlock,
        processParameters = cms.vstring(
            '25:onMode = off', # Turn off all H decays
            '25:oneChannel = 1 1 100 15 -15', # H->tau tau
            '25:onIfMatch = 15 -15',
            '35:onMode = off',
            '35:oneChannel = 1 1 100 22 22',  # Y->gamma gamma
            '35:onIfMatch = 22 22',
            'ResonanceDecayFilter:filter = on',
            'ResonanceDecayFilter:exclusive = on', #off: require at least the specified number of daughters, on: require exactly the specified number of daughters
            'ResonanceDecayFilter:mothers = 25,35', #list of mothers not specified -> count all particles in hard process+resonance decays (better to avoid specifying mothers when including leptons from the lhe in counting, since intermediate resonances are not gauranteed to appear in general
            'ResonanceDecayFilter:daughters = 15,15,22,22',
          ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'pythia8PSweightsSettings',
                                    'processParameters')
    )
)
"""

pythia_fragment_CP5['Ytt_Hgg'] = """
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *

generator = cms.EDFilter("Pythia8ConcurrentHadronizerFilter",
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13000.),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        pythia8PSweightsSettingsBlock,
        processParameters = cms.vstring(
            '25:onMode = off', # Turn off all H decays
            '25:oneChannel = 1 1 100 22 22', # H->gamma gamma
            '25:onIfMatch = 22 22',
            '35:onMode = off',
            '35:oneChannel = 1 1 100 15 -15',  # Y->tau tau
            '35:onIfMatch = 15 -15',
            'ResonanceDecayFilter:filter = on',
            'ResonanceDecayFilter:exclusive = on', #off: require at least the specified number of daughters, on: require exactly the specified number of daughters
            'ResonanceDecayFilter:mothers = 25,35', #list of mothers not specified -> count all particles in hard process+resonance decays (better to avoid specifying mothers when including leptons from the lhe in counting, since intermediate resonances are not gauranteed to appear in general
            'ResonanceDecayFilter:daughters = 15,15,22,22',
          ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'pythia8PSweightsSettings',
                                    'processParameters')
    )
)
"""

LHEproducer = """
import FWCore.ParameterSet.Config as cms
externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring('__GRIDPACK__'),
    nEvents = cms.untracked.uint32(5000),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh'),
    generateConcurrently = cms.untracked.bool(True)
)
"""
# Definitions
years   = ["2016", "2016APV", "2017", "2018"]
resType = ["Ygg_Htt", "Ytt_Hgg"]

# Mass ranges (Following mX > mY = 125)
mX_1 = [240, 280, 320, 360]
mY_1 = [60, 70, 80, 90, 100, 125, 150, 200, 250, 300]
mX_2 = [300, 400, 500, 600, 700, 800, 900, 1000]
mY_2 = [60]
mX_3 = [1200, 1400, 1600, 1800, 2000, 2200, 2400, 2500, 2600, 2800, 3000, 3500, 4000]
mY_3 = [60, 70, 80, 90, 100, 125,150, 250, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1600, 1800, 2000, 2200, 2400, 2500, 2600, 2800]

tot_events = 400000
version    = "2.6.5"

t_datasetname = {}
t_datasetname['Ygg_Htt'] = "NMSSM_XToYHTo2G2Tau_MX-<massX>_MY-<massY>_TuneCP5_13TeV-madgraph-pythia8" #"NMSSM_XYH_Y_gg_H_tautau_MX_<massX>_MY_<massY>_TuneCP5_13TeV-madgraph-pythia8"
t_datasetname['Ytt_Hgg'] = "NMSSM_XToYHTo2Tau2G_MX-<massX>_MY-<massY>_TuneCP5_13TeV-madgraph-pythia8" #"NMSSM_XYH_Y_tautau_H_gg_MX_<massX>_MY_<massY>_TuneCP5_13TeV-madgraph-pythia8"

gp = "/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/madgraph/V5_2.6.5/NMSSM_XYH/NMSSM_XToYH_MX_<massX>_MY_<massY>/v1/NMSSM_XToYH_MX_<massX>_MY_<massY>_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz" 

generators="Madgraph_" + version + "  Pythia8"
mcdb_id = '0' 
time = '2.1' 
size = '110' 

for i, year in enumerate(years):
    print("year = ", year)
        
    counter = 0
    for res in resType:
        with open(res+'_'+year+'.csv', 'w') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=',',
                                   quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csvwriter.writerow(['Dataset name','Events', 'fragment','notes','Generator','mcdbid','time','size'])

            if year == "2016APV":
                events = int(round(tot_events*0.54))
            elif year == "2016":
                events = int(round(tot_events*0.46))
            elif year == "2017":
                events = int(tot_events)
            elif year == "2018":
                events = int(tot_events)
                
        # get mass ranges (Following mX > mY + 125)
            for mX in mX_1:
                for mY in mY_1:
                    if mX <= mY + 125: continue                    
                    gridpacks, dataset_name, note = GetGridpacksAndDataset(gp, t_datasetname[res], res, mX, mY, 0)
                    if (gridpacks == None): continue
                    counter = counter + 1                    
                    final_fragment = GetFragments(LHEproducer, pythia_fragment_CP5[res], gridpacks, 0)
                    csvwriter.writerow([dataset_name, events, final_fragment, note, generators, mcdb_id, time, size])
                    
            for mX in mX_2:
                for mY in mY_2:
                    if mX <= mY + 125: continue                    
                    gridpacks, dataset_name, note = GetGridpacksAndDataset(gp, t_datasetname[res], res, mX, mY, 0)
                    if (gridpacks == None): continue
                    counter = counter + 1
                    final_fragment = GetFragments(LHEproducer, pythia_fragment_CP5[res], gridpacks, 0)
                    csvwriter.writerow([dataset_name, events, final_fragment, note, generators, mcdb_id, time, size])

            for mX in mX_3:
                for mY in mY_3:
                    if mX <= mY + 125: continue                    
                    gridpacks, dataset_name, note = GetGridpacksAndDataset(gp, t_datasetname[res], res, mX, mY, 0) #, res != "Ygg_Htt")
                    if (gridpacks == None): continue
                    counter = counter + 1
                    final_fragment = GetFragments(LHEproducer, pythia_fragment_CP5[res], gridpacks, 0)
                    csvwriter.writerow([dataset_name, events, final_fragment, note, generators, mcdb_id, time, size])
        

print("Datasets per year, process", float(counter)/2)
