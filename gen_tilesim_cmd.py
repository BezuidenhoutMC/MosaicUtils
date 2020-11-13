import numpy as np
import datetime
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument('-f', dest='file', 
			nargs = 1, 
			type = str, 
			help="Detections file",
			required=True)

options = parser.parse_args()
f = options.file[0]

with open(f) as json_file:
	data = json.load(json_file)

freq = str(data['beams']['ca_target_request']['tilings'][0]['reference_frequency'])
ra = str(data['beams']['ca_target_request']['tilings'][0]['target'].split(',')[2])
dec = str(data['beams']['ca_target_request']['tilings'][0]['target'].split(',')[3])
time = str(datetime.datetime.utcfromtimestamp(data['beams']['ca_target_request']['tilings'][0]['epoch'])).replace("-",".")
nbeams = str(data['beams']['ca_target_request']['tilings'][0]['nbeams'])
overlap = str(data['beams']['ca_target_request']['tilings'][0]['overlap'])

antennas = data['beams']['cb_antennas']
antenna_str = ''
for i in range(0,len(antennas)):
	num = antennas[i].strip("m")
	if i ==0:
		antenna_str += num
	else:
		antenna_str += ","+num

print "python tilesim.py --ants antenna.csv --freq "+ freq + " --source " +  ra + " " + dec + " --datetime "+ time + " --beamnum " + nbeams + " --verbose --overlap " + overlap + " --resolution 1 --size 1000 --subarray " + antenna_str

#python tilesim.py --ants antenna.csv --freq 1.284e9 --source 4:52:34.11 -17:59:23.4 --datetime 2020.07.16 11:24:17.802 --beamnum 384 --verbose --overlap 0.95 --resolution 1 --size 1000 --subarray
