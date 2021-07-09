import pandas as pd
import numpy as np
import requests
import re
import csv
import copy

# AToZHTo2L2B_bbH4F fragments
pythia_fragment_CP5 = """
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from Configuration.Generator.Pythia8aMCatNLOSettings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *

generator = cms.EDFilter("Pythia8HadronizerFilter",
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13000.),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8CP5SettingsBlock,
        pythia8aMCatNLOSettingsBlock,
        pythia8PSweightsSettingsBlock,
        processParameters = cms.vstring(
            'TimeShower:nPartonsInBorn = 2', #number of coloured particles (before resonance decays) in born matrix element
        ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'pythia8aMCatNLOSettings',
                                    'pythia8PSweightsSettings',
                                    'processParameters',
                                    )
    )
)
ProductionFilterSequence = cms.Sequence(generator)
"""

LHEproducer = """
import FWCore.ParameterSet.Config as cms
externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring('__GRIDPACK__'),
    nEvents = cms.untracked.uint32(1000),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
)
"""
# Definitions
years = ["2016", "2016APV", "2017", "2018"]
ranges = [
    "200p00_125p00_20p00",
    "510p00_130p00_20p00",
    "750p00_610p00_20p00",
]

tot_events = 30000
gridpacks_dict = {}
dataset_names = {}
version="2.6.5"
t_datasetname = "AToZHTo2L2B_<RANGE>_bbH4F_TuneCP5_13TeV-amcatnlo_pythia8"
t_gp = "/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/madgraph/V5_2.6.5/AToZHTo2L2B_<RANGE>_bbH4F_TuneCP5_13TeV-amcatnlo_pythia8/v1/AToZHTo2L2B_<RANGE>_bbH4F_TuneCP5_13TeV-amcatnlo_pythia8_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz"

for i, year in enumerate(years):
    with open('AToZHTo2L2B_bbH4F_'+year+'.csv', 'w') as csvfile:
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

        for r in ranges:
            gridpacks = copy.deepcopy(t_gp)
            gridpacks = gridpacks.replace("<RANGE>",r)
            dataset_name = copy.deepcopy(t_datasetname)
            dataset_name = dataset_name.replace("<RANGE>",r)
            tmp_fragment = copy.deepcopy(LHEproducer)
            tmp_fragment = tmp_fragment.replace("__GRIDPACK__",gridpacks)
            note = dataset_name.replace('_',' ')
            generators="Madgraph_" + version + "  Pythia8"
            mcdb_id = '0' # what is this?
            time = '0.3' # fixme
            size = '120' #fixme
            t_LHEproducer = copy.deepcopy(LHEproducer)
            final_fragment = t_LHEproducer.replace('__GRIDPACK__',gridpacks) + '\n' + pythia_fragment_CP5
            csvwriter.writerow([dataset_name, events, final_fragment, note, generators, mcdb_id, time, size])
