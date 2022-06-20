import pandas as pd
import numpy as np
import requests
import re
import csv
import copy
from os import path 

# HToZATo2L2B_ggH fragments
pythia_fragment_CP5 = """
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *
from Configuration.Generator.Pythia8aMCatNLOSettings_cfi import *
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
    nEvents = cms.untracked.uint32(5000),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh'),
    generateConcurrently = cms.untracked.bool(True)
)
"""
# Definitions
years = ["2016", "2016APV", "2017", "2018"]
ranges = [
80, 90, 100, 110, 120, 130, 140, # 1.5M
150, 155, 160 # 2.0M
]
charges = ["plus", "minus"]
def GetTotEvents(mass):
    if mass <= 140:
        return 1500000
    return 2000000

#tot_events = 30000
gridpacks_dict = {}
dataset_names = {}
version="2.6.5"
t_datasetname = "TTToH<CHARGE>ToCS_M-<RANGE>_TuneCP5_13TeV-amcatnlo-pythia8"
#t_gp = "/afs/cern.ch/work/s/savarghe/public/gridpacks/H<CHARGE>ToCS_M<RANGE>_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz"
t_gp = "/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/madgraph/V5_2.6.5/H<CHARGE>ToCS_M<RANGE>/v1/H<CHARGE>ToCS_M<RANGE>_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz"

id_2016    = 2902
id_2016APV = 2382
id_2017    = 2863
id_2018    = 2906

for i, year in enumerate(years):
    with open('ChargedHiggsToCS_'+year+'.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',',
                               quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(['prepid','Dataset name','Events', 'fragment','notes','Generator','mcdbid'])#,'time','size'])
        
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
        
        for r in ranges:
            tot_events = GetTotEvents(r)
            for c in charges:
                
                if year == "2016APV":
                    events = int(round(tot_events*0.54))
                elif year == "2016":
                    events = int(round(tot_events*0.46))
                elif year == "2017":
                    events = int(tot_events)
                elif year == "2018":
                    events = int(tot_events)

                gridpacks = copy.deepcopy(t_gp)
                gridpacks = gridpacks.replace("<RANGE>",str(r))
                gridpacks = gridpacks.replace("<CHARGE>",c)
                ### Check if gridpacks exist            
                gr_exists = path.exists(gridpacks)
                if (not gr_exists):
                    print("Path %s does not exist!" % gr_exists)
                #else:
                #    print("Gridpacks found!")
                dataset_name = copy.deepcopy(t_datasetname)
                dataset_name = dataset_name.replace("<RANGE>",str(r))
                dataset_name = dataset_name.replace("<CHARGE>",c)

                prepid = campaign+str(id_)
                
                print("prepid = %s, year = %s, mass = %s, charge = %s, events = %s, datasetName = %s" % (prepid, year, r, c, events, dataset_name))
            
                tmp_fragment = copy.deepcopy(LHEproducer)
                tmp_fragment = tmp_fragment.replace("__GRIDPACK__",gridpacks)
                note = dataset_name.replace('_',' ')
                generators="Madgraph_" + version + "  Pythia8"
                mcdb_id = '0' # 
                time = '2.8' 
                size = '128.5' 
                '''
                year_tag = "ULPAG%s" % year
                year_tag = year_tag.replace("20","")
                year_tag = year_tag.replace("APV","")
                tags = ['HEXO', 'HExtended', year_tag]
                print(tags)
                '''
                t_LHEproducer = copy.deepcopy(LHEproducer)
                final_fragment = t_LHEproducer.replace('__GRIDPACK__',gridpacks) + '\n' + pythia_fragment_CP5
                csvwriter.writerow([prepid, dataset_name, events, final_fragment, note, generators, mcdb_id])#, time, size])
                
                id_ = id_ + 1