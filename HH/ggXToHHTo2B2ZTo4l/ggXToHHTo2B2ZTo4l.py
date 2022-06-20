import pandas as pd
import numpy as np
import requests
import re
import csv
import copy
from os import path

# fragments
pythia_fragment_CP5 ="""
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
                                 '23:mMin = 0.05',
                                 '23:onMode = off',
                                 '23:onIfAny = 11 13 15', # only leptonic Z decays
                                 '25:m0 = 125.0',
                                 '25:onMode = off',
                                 '25:onIfMatch = 5 -5',
                                 '25:onIfMatch = 23 23',
                                 'ResonanceDecayFilter:filter = on',
                                 'ResonanceDecayFilter:exclusive = on', #off: require at least the specified number of daughters, on: require exactly the specified number of daughters
                                 'ResonanceDecayFilter:eMuAsEquivalent = off', #on: treat electrons and muons as equivalent
                                 'ResonanceDecayFilter:eMuTauAsEquivalent = on', #on: treat electrons, muons , and taus as equivalent
                                 'ResonanceDecayFilter:allNuAsEquivalent = off', #on: treat all three neutrino flavours as equivalent
                                 'ResonanceDecayFilter:mothers = 25,23', #list of mothers not specified -> count all particles in hard process+resonance decays (better to avoid specifying mothers when including leptons from the lhe in counting, since intermediate resonances are not gauranteed to appear in general
                                 'ResonanceDecayFilter:daughters = 5,5,11,11,11,11',
                             ),
                             parameterSets = cms.vstring('pythia8CommonSettings',
                                                         'pythia8CP5Settings',
                                                         'pythia8PSweightsSettings',
                                                         'processParameters'
                                                     )
                         )
                     )

ProductionFilterSequence = cms.Sequence(generator)
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
resType = ["Radion", "BulkGraviton"]
dict_ranges  = {
    "Radion"       : ["250", "260", "270", "280", "300", "320", "350", "400", "450", "500", "550", "600", "650", "700", "750", "800", "850", "900", "1000", "1100", "1200", "1300", "1400", "1500", "1600", "1700", "1800", "1900", "2000", "2200", "2400", "2600", "2800", "3000"],
    "BulkGraviton" : ["250", "260", "270", "280", "300", "320", "350", "400", "450", "500", "550", "600", "650", "700", "750", "800", "850", "900", "1000", "1250", "1500", "1750", "2000", "2500", "3000"],
}

print("Number of samples: \n Radion = %s \n BulkGraviton = %s" % (str(len(dict_ranges["Radion"])), str(len(dict_ranges["BulkGraviton"]))))

tot_events = 400000
version    = "2.6.5"

t_datasetname = "GluGluTo<RESTYPE>ToHHTo2B2ZTo4L_M-<RANGE>_TuneCP5_PSWeights_narrow_13TeV-madgraph-pythia8"

dict_gp = {
    "Radion":"/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/madgraph/V5_2.6.5/GF_Spin_0/Radion_hh_narrow_M<RANGE>/v1/Radion_hh_narrow_M<RANGE>_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",
    "BulkGraviton":"/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/madgraph/V5_2.6.5/GF_Spin_2/BulkGraviton_hh_GF_HH_narrow_M<RANGE>/v1/BulkGraviton_hh_GF_HH_narrow_M<RANGE>_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz",
}

for i, year in enumerate(years):
    print("year = ", year)
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

            for r in dict_ranges[res]:
                gridpacks = copy.deepcopy(dict_gp[res])
                gridpacks = gridpacks.replace("<RANGE>",r)
                ### Check if gridpacks exist            
                gr_exists = path.exists(gridpacks)
                if (not gr_exists):
                    print("[%s] Path %s does not exist!" % gridpacks)
                #else:
                #    print("[%s] Path %s exists!" % (res, gridpacks))

                dataset_name = copy.deepcopy(t_datasetname)
                dataset_name = dataset_name.replace("<RANGE>",r).replace("<RESTYPE>", res)

                if 1: print("[%s] Dataset name: %s" % (res,dataset_name))

                tmp_fragment = copy.deepcopy(LHEproducer)
                tmp_fragment = tmp_fragment.replace("__GRIDPACK__",gridpacks)
                note = dataset_name.replace('_',' ')
                generators="Madgraph_" + version + "  Pythia8"
                mcdb_id = '0' 
                time = '1.8' 
                size = '122' 
                t_LHEproducer = copy.deepcopy(LHEproducer)
                final_fragment = t_LHEproducer.replace('__GRIDPACK__',gridpacks) + '\n' + pythia_fragment_CP5
                csvwriter.writerow([dataset_name, events, final_fragment, note, generators, mcdb_id, time, size])
        
