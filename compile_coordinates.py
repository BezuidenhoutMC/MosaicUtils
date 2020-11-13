import json
import os
import os.path
import psrchive
from subprocess import Popen, PIPE


data = []
os.environ["TERM"] = "dumb"
for n in range(0,58):
	for i in range(0,12):
		fname = "n"+str(n)+"b"+str(i).zfill(2)+'_2020_07_16_12:45:47.fil.pazi'
		if os.path.isfile(fname):
			log = "n"+str(n)+"_run_summary.json"
			with open(log) as json_file:
				data = json.load(json_file)

			#cmd = "psrstat -q -c '{$on:max-$off:avg}' -j DFTp " + fname
			cmd = "psrstat -q -c snr -j DFTp " + fname
			pipe = Popen(cmd, shell=True, bufsize=1, stdout=PIPE).stdout
			value =  pipe.readline().strip("\n").strip(" ").strip("snr=")
			ra = data['beams']["list"][i]["ra_hms"]
			dec = data['beams']["list"][i]["dec_dms"]
			#print fname[0:3]+"b"+str(i),ra,dec,value
			print ra,dec,value
