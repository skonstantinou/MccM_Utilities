import pandas as pd
import numpy as np
import requests
import re
import csv
import copy
from os import path

def GetRange(filaname):
    rangeList = []
    infile = open(filaname, 'r')
    lines = infile.readlines()
    for i,l in enumerate(lines):
        _range = copy.deepcopy(l)
        _range = _range.replace("/eos/cms/store/group/phys_higgs/HiggsExo/kjaffel/HToZATo2L2B_ggfusion_b-associatedproduction/waiting_for_submission_to_mcm/bbH/HToZATo2L2B_", "")
        _range = _range.replace("_bbH4F_TuneCP5_13TeV_pythia8_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz", "")
        _range = _range.replace(" ","")
        _range = _range.replace("\n","")
        rangeList.append(_range)
    return rangeList

# HToZATo2L2B_bbH4F fragments
pythia_fragment_CP5 = """
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
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh'),
    generateConcurrently = cms.untracked.bool(True)
)
"""
# Definitions
years = ["2016", "2016APV", "2017", "2018"]

ranges = GetRange("notSubmitted_bbH.txt")
print("samples = ", len(ranges))

# priority samples
'''
ranges = [
    "200p00_100p00_20p00",
    "250p00_50p00_20p00",
    "250p00_100p00_20p00",
    "300p00_50p00_20p00",
    "300p00_100p00_20p00",
    "300p00_200p00_20p00",
    "500p00_50p00_20p00",
    "500p00_100p00_20p00",
    "500p00_200p00_20p00",
    "500p00_300p00_20p00",
    "500p00_400p00_20p00",
    "650p00_50p00_20p00",
    "800p00_50p00_20p00",
    "800p00_100p00_20p00",
    "800p00_200p00_20p00",
    "800p00_400p00_20p00",
    "800p00_700p00_20p00",
    "1000p00_50p00_20p00",
    "1000p00_200p00_20p00",
    "1000p00_500p00_20p00",
    "200p00_125p00_20p00",
    "510p00_130p00_20p00",
    "750p00_610p00_20p00",
]
'''

tot_events = 30000
gridpacks_dict = {}
dataset_names = {}
version="2.6.5"
# t_datasetname = "HToZATo2L2B_<RANGE>_TuneCP5_bbH4F_13TeV-mcatnlo-pythia8" #NLO
t_datasetname = "HToZATo2L2B_<RANGE>_TuneCP5_bbH4F_13TeV-madgraph-pythia8"
# priority
#t_gp = "/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/madgraph/V5_2.6.5/HToZATo2L2B_<RANGE>_bbH4F_TuneCP5_13TeV-amcatnlo_pythia8/v1/HToZATo2L2B_<RANGE>_bbH4F_TuneCP5_13TeV-amcatnlo_pythia8_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz"
#t_gp = "/eos/cms/store/group/phys_higgs/HiggsExo/kjaffel/HToZATo2L2B_ggfusion_b-associatedproduction/waiting_for_submission_to_mcm/bbH/HToZATo2L2B_<RANGE>_bbH4F_TuneCP5_13TeV_pythia8_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz"
t_gp = "/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/madgraph/V5_2.6.5/HToZATo2L2B_<RANGE>_bbH4F_TuneCP5_13TeV_pythia8/v1/HToZATo2L2B_<RANGE>_bbH4F_TuneCP5_13TeV_pythia8_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz"

id_2016    = 2979+10
id_2016APV = 2460+10
id_2017    = 2913+10
id_2018    = 2959+10

for i, year in enumerate(years):
    with open('HToZATo2L2B_bbH4F_'+year+'.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',',
                               quotechar='"', quoting=csv.QUOTE_MINIMAL)
        #csvwriter.writerow(['prepid','Dataset name','Events', 'fragment','notes','Generator','mcdbid','time','size'])
        csvwriter.writerow(['prepid','Dataset name','Events', 'fragment','notes','Generator','mcdbid'])


        if year == "2016":
            campaign = "HIG-RunIISummer20UL16wmLHEGEN-0"
            id_ = id_2016
        elif year == "2016APV":
            campaign = "HIG-RunIISummer20UL16wmLHEGENAPV-0"
            id_ = id_2016APV
        elif year == "2017":
            campaign = "HIG-RunIISummer20UL17wmLHEGEN-0"
            id_ = id_2017
        elif year == "2018":
            campaign = "HIG-RunIISummer20UL18wmLHEGEN-0"
            id_ = id_2018

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
            ### Check if gridpacks exist            
            gr_exists = path.exists(gridpacks)
            if (not gr_exists):
                print("Path %s does not exist!" % gridpacks)

            dataset_name = copy.deepcopy(t_datasetname)
            rangeList = r.split("_") 
            # HToZATo2L2B_MH-1000p00_MA-200p00_tb-20p00_TuneCP5_bbH4F_13TeV-mcatnlo-pythia8
            rangeType = "MH-%s_MA-%s_tb-%s" % (rangeList[0], rangeList[1], rangeList[2])
            dataset_name = dataset_name.replace("<RANGE>",rangeType)

            ### Check if filename exist
            dataset_names_txt = open("dataset_names_bbH_NOT_submitted.txt", "r")
            dNameExists = False
            for line in dataset_names_txt:
                if re. search(dataset_name, line):
                    dNameExists = True
            if (dNameExists == False):
                print("Dataset name %s does not exist!" % dataset_name)

            prepid = campaign+str(id_)

            print("prepid = %s, year = %s, mass = %s, events = %s, datasetName = %s" % (prepid, year, r, events, dataset_name))
            
            tmp_fragment = copy.deepcopy(LHEproducer)
            tmp_fragment = tmp_fragment.replace("__GRIDPACK__",gridpacks)
            note = dataset_name.replace('_',' ')
            generators="Madgraph_" + version + "  Pythia8"
            mcdb_id = '0' 
            time = '2.7' 
            size = '125' 
            t_LHEproducer = copy.deepcopy(LHEproducer)
            final_fragment = t_LHEproducer.replace('__GRIDPACK__',gridpacks) + '\n' + pythia_fragment_CP5
            #csvwriter.writerow([prepid, dataset_name, events, final_fragment, note, generators, mcdb_id, time, size])
            csvwriter.writerow([prepid, dataset_name, events, final_fragment, note, generators, mcdb_id])
            
            id_ = id_ + 1
