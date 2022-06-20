# From Alp Akpinar
### Get the request information and create csv files.
import csv
import argparse
from container import request_information # Holds all information about the requests
from pprint import pprint
from os import path

parser = argparse.ArgumentParser()
parser.add_argument("-y", "--years", choices=[2017,2018], nargs='*', type=int,
                              required=True, help="MC year condition (2017-2018)" )

args = parser.parse_args()
years = args.years

for year in years:
    requests = request_information[year]
    with open('ChargedHiggsHPlusTB_{__YEAR__}.csv'.format(__YEAR__=year), 'w_') as csvfile:
        #writer = csv.DictWriter(f, fieldnames=['Dataset name', 'Events', 'Filter efficiency', 'Match efficiency','fragment', 'notes', 'generator'], extrasaction='ignore')
        csvwriter = csv.writer(csvfile, delimiter=',',
                               quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(['Dataset name','Events', 'fragment','notes','Generator','time','size'])
        #writer.writeheader()
        for mass_point in requests.keys():            
            data = requests[mass_point]
            print("mass = %s, events = %s, datasetName = %s" % (mass_point, data["Events"], data["Dataset name"]))
            ### Check if gridpacks exist
            gridpacks = data["gridpack"]
            gr_exists = path.exists(gridpacks)
            if (not gr_exists):
                print("Path %s does not exist!" % gr_exists)
            else:
                print("Gridpacks found!")
            #writer.writerow(data)
            csvwriter.writerow([data["Dataset name"], data["Events"], data['fragment'], data["notes"], data["generator"], data["Time event"], data["Size event"]])
