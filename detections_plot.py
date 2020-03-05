#!/usr/bin/env python
'''

'''
import numpy as np
import argparse
import configparser
import matplotlib.patches as ptch
from matplotlib import pyplot as plt
from astropy.coordinates import SkyCoord
import astropy.units  as u

parser = argparse.ArgumentParser()
parser.add_argument('-c', dest='coords', nargs = 1, type = str, help="Beam coordinates file",
					required=True)
parser.add_argument('-f', dest='file', nargs = 1, type = str, help="Candidate file")
parser.add_argument('--w',dest = 'el_width',nargs = 1, type = float)
parser.add_argument('--h',dest = 'el_height',nargs = 1, type = float)
parser.add_argument('--a',dest = 'el_angle',nargs = 1, type = float)
parser.add_argument('--d',dest = 'dets',nargs = '+', type = int)
parser.add_argument('--k',dest = 'known', nargs = 2, type=float, metavar=('RA', 'DEC'),
					action='append',help='source position in RADEC or AziAlt')

options= parser.parse_args()

if options.file is not None:
	config = configparser.ConfigParser()
	config.read(options.file)
	el_height = float(config['DEFAULT']['EL_HEIGHTS'].split(',')[0])
	el_width = float(config['DEFAULT']['EL_WIDTHS'].split(',')[0])
	el_angle = float(config['DEFAULT']['EL_ANGLES'].split(',')[0])

else:
	if options.el_height == None or options.el_width == None or options.el_angle == None:
		print('Error: If you are not using a config file, you have to specify the the beam height, width, and '
				'orientation angle with command line options.')
		exit()
	el_height = options.el_height[0]
	el_width = options.el_width[0]
	el_angle = options.el_angle[0]

el_width/=3600
el_height/=3600

pulse = np.genfromtxt(options.coords[0],delimiter=' ',dtype=float,names=["RA","Dec"],encoding="ascii")

fig,ax = plt.subplots(1,1)
ax.scatter(pulse["RA"],pulse["Dec"],s=3)

if options.known is not None:
	for sourceCoord in options.known:
		ax.scatter(sourceCoord[0],sourceCoord[1],marker='x',color='red')

for i in range(0,len(pulse["RA"])):
	if i in options.dets:
		e=ptch.Ellipse(xy=(pulse["RA"][i],pulse["Dec"][i]),width=2*el_width,height=2*el_height,
					   angle=el_angle,fill=True,color='magenta')
		ax.add_artist(e)
	
	e=ptch.Ellipse(xy=(pulse["RA"][i],pulse["Dec"][i]),width=2*el_width,height=2*el_height,
				   angle=el_angle,fill=False,color='green')
	ax.add_artist(e)
	
plt.xlabel('RA (deg)')
plt.ylabel('Dec (deg)')

plt.show()


