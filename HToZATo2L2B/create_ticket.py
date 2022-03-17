import sys
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import McM
from json import dumps

mcm = McM(dev=False)
#mcm = McM(dev=True) 

# Script creates a new ticket in MccM.
# Fefine list of modifications

#step = [44,44,44,42,40]
step = [39,39,39,39,39]

a=3180
for i in range(len(step)):	        
	b = a+step[i]
	print("HIG-RunIISummer20UL18wmLHEGEN-0" + str(a) + ", RunIISummer20UL18wmLHEGEN-0" + str(b))
	new_mccm = {'pwg': 'HIG', 'prepid': 'HIG', 'requests': [['HIG-RunIISummer20UL18wmLHEGEN-0' + str(a),
                                                                 'HIG-RunIISummer20UL18wmLHEGEN-0' + str(b)]], 'chains': ['chain_RunIISummer20UL18wmLHEGEN_flowRunIISummer20UL18SIM_flowRunIISummer20UL18DIGIPremix_flowRunIISummer20UL18HLT_flowRunIISummer20UL18RECO_flowRunIISummer20UL18MiniAODv2_flowRunIISummer20UL18NanoAODv9'], 'block': '3'}
        #print("HIG-RunIISummer20UL16wmLHEGENAPV-0" + str(a) + ", RunIISummer20UL16wmLHEGENAPV-0" + str(b)) 
	#new_mccm = {'pwg': 'HIG', 'prepid': 'HIG', 'requests': [['HIG-RunIISummer20UL16wmLHEGENAPV-0' + str(a),
        #                                                         'HIG-RunIISummer20UL16wmLHEGENAPV-0' + str(b)]], 'chains': ['chain_RunIISummer20UL16wmLHEGENAPV_flowRunIISummer20UL16SIMAPV_flowRunIISummer20UL16DIGIPremixAPV_flowRunIISummer20UL16HLTAPV_flowRunIISummer20UL16RECOAPV_flowRunIISummer20UL16MiniAODAPVv2_flowRunIISummer20UL16NanoAODAPVv9'], 'block': '3'}
	mcm.put('mccms', new_mccm)
	a = b+1

	
