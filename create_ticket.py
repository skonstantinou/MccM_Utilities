import sys
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import McM
from json import dumps

mcm = McM(dev=False)

# Script creates a new ticket in MccM.
# Fefine list of modifications

step = [40,40,40,36]

a=1972 
for i in range(len(step)):	
	b = a+step[i]
	print("HIG-RunIISummer20UL16wmLHEGEN-0" + str(a) + ", RunIISummer20UL16wmLHEGEN-0" + str(b))
	new_mccm = {'pwg': 'HIG', 'prepid': 'HIG', 'requests': [['HIG-RunIISummer20UL16wmLHEGEN-0' + str(a),
'HIG-RunIISummer20UL16wmLHEGEN-0' + str(b)]], 'chains': ['chain_RunIISummer20UL16wmLHEGEN_flowRunIISummer20UL16SIM_flowRunIISummer20UL16DIGIPremix_flowRunIISummer20UL16HLT_flowRunIISummer20UL16RECO_flowRunIISummer20UL16MiniAODv2_flowRunIISummer20UL16NanoAODv9'], 'block': '3'}
	mcm.put('mccms', new_mccm)
	a = b+1

	
