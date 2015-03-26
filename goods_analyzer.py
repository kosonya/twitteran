#!/usr/bin/env python
# -*- coding: utf8 -*-

import re
import json
import pickle
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap



def main():
	f = open("/mnt/data/twitterdump/relevant_tweets", "r")
	data = pickle.load(f)
	f.close()
	lats = []
	lons = []
	for tweet in data:
		lon, lat = tweet['retweeted_status']['coordinates']['coordinates']
		lats.append(lat)
		lons.append(lon)
		
	print len(lons)
	lons = np.array(lons)
	lats = np.array(lats)


	m = Basemap(projection='merc',llcrnrlat=-80,urcrnrlat=80,\
				llcrnrlon=-180,urcrnrlon=180,lat_ts=20,resolution='c')

	m.drawcoastlines()
	m.fillcontinents(color='0.8')
	# draw parallels and meridians.
	m.drawparallels(np.arange(-90.,91.,30.))
	m.drawmeridians(np.arange(-180.,181.,60.))
	#m.drawmapboundary(fill_color='aqua')
	
	xs,ys = m(lons,lats)

	m.plot(xs, ys, latlon=False, linestyle='circle marker', marker='o', markerfacecolor='blue', markersize=5)

	plt.title("RTs matching ( rain|storm|cloud| thunder|hurricane|tornado| hail| snow|flood| snow) 03/24/15")


	plt.show()

if __name__ == "__main__":
	main()

