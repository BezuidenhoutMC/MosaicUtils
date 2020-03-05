#!/usr/bin/env python
'''
Code to plot the MeerKAT primary beam and TABs for a given pointing
configuration.
'''

#Size of primary beam in deg at various frequencies (uncorrected):
freqs = [856,963,1070,1177,1284,1391,1498,1605] 
h = [1.70,1.56,1.37,1.23,1.11,1.02,0.96,0.90]
'''NOTE: I assume a circular primary beam with diameter equal to
   the size in the horizontal polarisation direction. There'll be
   a small error due to this.
'''
# v = [1.68,1.48,1.33,1.17,1.05,0.98,0.94,0.90]


import numpy as np
import argparse
import matplotlib.patches as ptch
from matplotlib import pyplot as plt
import math
import configparser

latitude = np.deg2rad(-30.721)


parser = argparse.ArgumentParser()
parser.add_argument('-f', dest='file', nargs = 1, type = str, help="Candidate file",required=True)
options= parser.parse_args()

config = configparser.ConfigParser()
config.read(options.file)
fnames = config['DEFAULT']['COORD_FILES'].split(',')
decs = config['DEFAULT']['DECS'].split(',')
has = config['DEFAULT']['HOUR_ANGLES'].split(',')
el_heights = config['DEFAULT']['EL_HEIGHTS'].split(',')
el_widths = config['DEFAULT']['EL_WIDTHS'].split(',')
el_angles = config['DEFAULT']['EL_ANGLES'].split(',')


if len(decs) == 1:
	axes = [0]
	f,axis = plt.subplots(len(decs),1,sharex=False,facecolor='w')	
	axes[0] = axis
else:
	f,axes = plt.subplots(len(decs),1,sharex=False,facecolor='w')

for i in range (0,len(decs)):
	print('----'+str(i)+'--------------------------')

	filename = fnames[i]
	decs[i] = float(decs[i])
	has[i] = np.deg2rad(float(has[i]))
	el_heights[i] = float(el_heights[i])/3600
	el_widths[i] = float(el_widths[i])/3600
	el_angles[i] = float(el_angles[i])

	pulse = np.genfromtxt(filename,delimiter=' ',dtype=None,names=["RA","Dec"],encoding="ascii")

	tile_height=max(pulse["Dec"])-min(pulse["Dec"])
	tile_width=max(pulse["RA"])-min(pulse["RA"])
	tile_area = math.pi*tile_height*tile_width/4

	print("Height at "+str(decs[i])+"deg Dec:  " + str(tile_height) + " deg")
	print("Width at "+str(decs[i])+"deg Dec:  " + str(tile_width) + " deg")
	print("Area at "+str(decs[i])+"deg Dec:  " + str(tile_area) + " deg^2")
	print("")
	
	axes[i].annotate(str(round(tile_area,3))+'\ndeg^2',xy=(np.median(pulse["RA"]),np.median(pulse["Dec"])),bbox=dict(boxstyle='round,pad=0.2', fc='yellow', alpha=0.3))


	sc=axes[i].scatter(pulse["RA"],pulse["Dec"],s=3)
	plt.xlabel("RA (deg)")
	plt.ylabel("Dec (deg)")

	for q in range(0,len(pulse["RA"])):
		e=ptch.Ellipse(xy=(pulse["RA"][q],pulse["Dec"][q]),
		width=2*el_widths[i],height=2*el_heights[i],angle=el_angles[i],fill=False,color='green')
		axes[i].add_artist(e)


	boresight_RA = np.mean(pulse["RA"])
	boresight_Dec = decs[i]

	sin_boresight_alt = (np.sin(np.deg2rad(decs[i]))*np.sin(latitude))+(np.cos(np.deg2rad(decs[i]))*np.cos(latitude)*np.cos(has[i]))
	boresight_alt = np.arcsin(sin_boresight_alt) 

	# if decs[i] > 0:
	#	 boresight_alt = 2*math.pi - boresight_alt

	cos_boresight_azim = (np.sin(np.deg2rad(decs[i])) - np.sin(boresight_alt)*np.sin(latitude)) / (np.cos(boresight_alt) *np.cos(latitude))
	if cos_boresight_azim > 1:
		cos_boresight_azim = 1
	if cos_boresight_azim < -1:
			cos_boresight_azim = -1	

	boresight_azim = np.arccos(cos_boresight_azim)

	color=plt.cm.rainbow(np.linspace(0,1,len(h)))

	for q in range(0,len(h)):
		A0 = boresight_azim - 0.5*np.deg2rad(h[q])
		A1 = boresight_azim + 0.5*np.deg2rad(h[q])

		sinRA0 = -np.sin(A0)*np.sin(boresight_alt)/np.cos(np.deg2rad(decs[i]))
		if sinRA0 > 1:
			sinRA0 = 1
		if sinRA0 < -1:
			sinRA0 = -1

		RA0 = np.arcsin(sinRA0)

		sinRA1 = -np.sin(A1)*np.sin(boresight_alt)/np.cos(np.deg2rad(decs[i]))
		if sinRA1 > 1:
			sinRA1 = 1
		if sinRA1 < -1:
			sinRA1 = -1

		RA1 = np.arcsin(sinRA1)
		WIDTH = np.rad2deg(RA1-RA0)

		HEIGHT = h[q]

		e=ptch.Ellipse(xy=(pulse["RA"][0],pulse["Dec"][0]),
		width=WIDTH,height=HEIGHT,angle=0,fill=False,color=color[q])

		axes[i].add_artist(e)


	axes[i].set_ylim(decs[i]-tile_height,decs[i]+tile_height)
	axes[i].set_xlim(np.mean(pulse["RA"])-tile_width,np.mean(pulse["RA"])+tile_width)

plt.tight_layout()
plt.savefig('Prim_beams.png',dpi=1000)
plt.show()

plt.close()
