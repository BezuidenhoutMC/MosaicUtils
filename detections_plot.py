#!/usr/bin/env python

import numpy as np
import argparse
import matplotlib.patches as ptch
from matplotlib import pyplot as plt
from astropy.coordinates import SkyCoord
import astropy.units  as u

parser = argparse.ArgumentParser()
parser.add_argument('-f', dest='file', nargs = 1, type = str, help="Beam coordinates file",required=True)
parser.add_argument('--w',dest = 'el_width',nargs = 1, type = float, required = True)
parser.add_argument('--h',dest = 'el_height',nargs = 1, type = float, required = True)
parser.add_argument('--a',dest = 'el_angle',nargs = 1, type = float, required = True)
parser.add_argument('--d',dest = 'dets',nargs = '+', type = int, required = False)
options= parser.parse_args()

options.el_width[0]/=3600
options.el_height[0]/=3600

pulse = np.genfromtxt(options.file[0],delimiter=' ',dtype=None,names=["RA","Dec"],encoding="ascii")

ax = plt.gca()
sc=plt.scatter(pulse["RA"],pulse["Dec"],s=3)
for i in range(0,len(pulse["RA"])):
	if i in options.dets:
		e=ptch.Ellipse(xy=(pulse["RA"][i],pulse["Dec"][i]),width=2*options.el_width[0],height=2*options.el_height[0],angle=options.el_angle[0],fill=True,color='magenta')
		ax.add_artist(e)
	e=ptch.Ellipse(xy=(pulse["RA"][i],pulse["Dec"][i]),width=2*options.el_width[0],height=2*options.el_height[0],angle=options.el_angle[0],fill=False,color='green')
	ax.add_artist(e)
	
plt.xlabel('RA (deg)')
plt.ylabel('Dec (deg)')

#RAs = ["16:00:54.84", "16:00:40.08","16:01:09.59","16:00:45.25","16:01:00.00"]
#Decs = ["-50:44:22.7", '-50:45:19.5', '-50:43:25.7','-50:43:59.3','-50:43:02.4']
#RAs = ["19:35:31.26", "19:35:19.87","19:32:55.45", "19:33:18.33"]
#Decs = ["-62:07:49.2", '-62:07:13.0', '-62:21:03.6',"-62:22:17.4"]


#for i in range(0,len(RAs)):
#	co = SkyCoord(RAs[i],Decs[i], frame="icrs",unit=(u.hourangle,u.deg))
#	plt.scatter(co.ra.deg,co.dec.deg,marker='x',color='red',zorder=7)	
plt.show()


