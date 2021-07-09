import pandas as pd
import numpy as np
import requests
import re
import csv
import copy

# HToZATo2L2B_ggH fragments
pythia_fragment_CP5 = """
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
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
        pythia8PSweightsSettingsBlock,
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8CP5Settings',
                                    'pythia8PSweightsSettings',
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
"200p00_100p00_1p50",
"250p00_50p00_1p50",
"250p00_100p00_1p50",
"300p00_50p00_1p50",
"300p00_100p00_1p50",
"300p00_200p00_1p50",
"500p00_50p00_1p50",
"500p00_100p00_1p50",
"500p00_200p00_1p50",
"500p00_300p00_1p50",
"500p00_400p00_1p50",
"650p00_50p00_1p50",
"800p00_50p00_1p50",
"800p00_100p00_1p50",
"800p00_200p00_1p50",
"800p00_400p00_1p50",
"800p00_700p00_1p50",
"1000p00_50p00_1p50",
"1000p00_200p00_1p50",
"1000p00_500p00_1p50",
"200p00_125p00_1p50",
"510p00_130p00_1p50",
"750p00_610p00_1p50",
]

tot_events = 30000
gridpacks_dict = {}
dataset_names = {}
version="2.6.5"
t_datasetname = "GluGluToHToZATo2L2B_<RANGE>_TuneCP5_13TeV-madgraph-pythia8"
t_gp = "/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/madgraph/V5_2.6.5/HToZATo2L2B_<RANGE>_ggH_TuneCP5_13TeV_pythia8/v1/HToZATo2L2B_<RANGE>_ggH_TuneCP5_13TeV_pythia8_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz"

for i, year in enumerate(years):
    with open('HToZATo2L2B_ggH_'+year+'.csv', 'w') as csvfile:
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
            rangeList = r.split("_")
            # GluGluToHToZATo2L2B_MH-1000p00_MA-200p00_tb-1p50_TuneCP5_13TeV-madgraph-pythia8
            rangeType = "MH-%s_MA-%s_tb-%s" % (rangeList[0], rangeList[1], rangeList[2])
            dataset_name = dataset_name.replace("<RANGE>",rangeType)
            print("datasetName = ", dataset_name)
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
