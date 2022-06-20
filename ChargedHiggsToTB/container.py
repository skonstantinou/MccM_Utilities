# From Alp Akpinar

import os
from pprint import pprint

pjoin = os.path.join

# Fragments
pythia_fragment = '''
from Configuration.Generator.Pythia8CommonSettings_cfi import *
from Configuration.Generator.PSweightsPythia.PythiaPSweightsSettings_cfi import *
from Configuration.Generator.Pythia8aMCatNLOSettings_cfi import *
from Configuration.Generator.MCTunes2017.PythiaCP5Settings_cfi import *

generator = cms.EDFilter("Pythia8HadronizerFilter",
    maxEventsToPrint = cms.untracked.int32(1),
    pythiaPylistVerbosity = cms.untracked.int32(1),
    filterEfficiency = cms.untracked.double(1.0),
    pythiaHepMCVerbosity = cms.untracked.bool(False),
    comEnergy = cms.double(13000.),
    PythiaParameters = cms.PSet(
        pythia8CommonSettingsBlock,
        pythia8PSweightsSettingsBlock,
        pythia8CP5SettingsBlock,
        pythia8aMCatNLOSettingsBlock,
        processParameters = cms.vstring(
            'TimeShower:nPartonsInBorn = 2', #number of coloured particles (before resonance decays) in born matrix element
            'Higgs:useBSM = on', ## enable handling of bsm particles
            'SLHA:keepSM = on', # read properties from lhe
            'SLHA:minMassSM = 100.', # as above
            '37:mayDecay = on', ## decay of the ch higgs
            '37:onMode = off',
            '37:onIfAny = 6',
            '37:doForceWidth = on' ## make it with a width
        ),
        parameterSets = cms.vstring('pythia8CommonSettings',
                                    'pythia8PSweightsSettings',
                                    'pythia8CP5Settings',
                                    'pythia8aMCatNLOSettings',
                                    'processParameters',
                                    )
    )
)
'''

lhe_fragment = '''import FWCore.ParameterSet.Config as cms

# link to card:
# __LINK__

externalLHEProducer = cms.EDProducer("ExternalLHEProducer",
    args = cms.vstring('__GRIDPACK__'),
    nEvents = cms.untracked.uint32(5000),
    numberOfParameters = cms.uint32(1),
    outputFile = cms.string('cmsgrid_final.lhe'),
    scriptName = cms.FileInPath('GeneratorInterface/LHEInterface/data/run_generic_tarball_cvmfs.sh')
)

__PYTHIA_FRAGMENT__
'''

# Link to proc card on GitHub
proc_card_link = 'https://github.com/cms-sw/genproductions/tree/705976d5de7ee8230d5a1a0b1d62890860b93103/bin/MadGraph5_aMCatNLO/cards/production/2017/13TeV/ChargedHiggs_TB/ChargedHiggs_TB_NLO/ChargedHiggs_TB_NLO_proc_card.dat'

# Mass points (M=300 already done by Gouranga)
mass_points = [200, 220, 250, 300, 350, 400, 500, 600, 700, 800, 1000, 1250, 1500, 1750, 2000, 2500, 3000]

# Gridpack locations at cvmfs
gridpack_template = '/cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/madgraph/V5_2.6.5/ChargedHiggs_TB_NLO_M{__MASS_POINT__}/v1/ChargedHiggs_TB_NLO_M{__MASS_POINT__}_slc6_amd64_gcc630_CMSSW_9_3_16_tarball.tar.xz'
gridpack_locs = {}

for mass_point in mass_points:
    gridpack_locs[mass_point] = gridpack_template.format(__MASS_POINT__ = mass_point)

# Dataset names
datasetname_template = 'ChargedHiggs_HplusTB_HplusToTB_M-{__MASS_POINT__}_TuneCP5_13TeV_amcatnlo_pythia8'
datasetnames = {}

for mass_point in mass_points:
    datasetnames[mass_point] = datasetname_template.format(__MASS_POINT__ = mass_point)

# Fill request information for 2017 and 2018
request_information = {}
for year in [2017,2018]:
    request_information[year] = {}
    for mass_point in mass_points:
        gridpack_path = gridpack_locs[mass_point]
        dataset_name = datasetnames[mass_point]
        request_information[year][mass_point] = {
            'gridpack' : gridpack_path,
            'Events' : 10000000, # 10M events for each mass point
            'Filter efficiency' : 1.0, # random value for now, check later
            'Match efficiency' : 1.0, # random value for now, check later
            'proc_card_link' : proc_card_link,
            'fragment' : lhe_fragment.replace('__LINK__', proc_card_link).replace('__PYTHIA_FRAGMENT__', pythia_fragment).replace('__GRIDPACK__', gridpack_path),
            'generator' : 'Madgraph+Pythia8',
            'Dataset name' : dataset_name,
            'notes' : dataset_name.split('_'),
            'Time event' : 4.5,
            'Size event' : 150
        }
