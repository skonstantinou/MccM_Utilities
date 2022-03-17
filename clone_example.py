import sys
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')
from rest import McM
from json import dumps

mcm = McM(dev=False)

# Script clones a request to other campaign.
# Fefine list of modifications
# If member_of_campaign is different, it will clone to other campaign
modifications = {#'extension': 1,
                 'total_events': 50000,
                 'member_of_campaign': 'RunIISummer20UL18pLHEGEN'}

request_prepid_to_clone = "HIG-RunIISummer20UL16pLHEGEN-"
for i in range(4,11):
	if i < 10:	
		prid = request_prepid_to_clone + "0000" + str(i)
	else:
		prid = request_prepid_to_clone + "000" + str(i)
	print(prid)
	# Get a request object which we want to clone
	request = mcm.get('requests', prid)
	print(request)
	# Make predefined modifications
	for key in modifications:
		request[key] = modifications[key]

	clone_answer = mcm.clone_request(request)
	if clone_answer.get('results'):
		print('Clone PrepID: %s' % (clone_answer['prepid']))
	else:
		print('Something went wrong while cloning a request. %s' % (dumps(clone_answer)))
