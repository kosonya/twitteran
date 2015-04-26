#!/usr/bin/env python
# -*- coding: utf8 -*-

import re
import json
import pickle
import dateutil.parser
import math

def haversine_dist(p1, p2):
	lat1, lon1 = map(math.radians, p1)
	lat2, lon2 = map(math.radians, p2)
	earth_radius = 6367.0
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = math.pow(math.sin(dlon/2.0), 2) + math.cos(lon1) * math.cos(lon2) * math.pow(math.sin(dlat/2.0), 2)
	c = 2.0 * math.asin(math.sqrt(a))
	km = earth_radius * c
	return km

def main():
	f_src = open("../twitterdump/dump_mar_31_9_10_with_geo", "r")

	start_timestamp = dateutil.parser.parse("Tue Mar 31 18:45:01 +0000 2015")
	stop_timestamp = dateutil.parser.parse("Wed Apr 01 23:45:01 +0000 2015")
	geo_center = (39.079908, -101.959464)
	geo_radius = 2000

	#keywords = re.compile("( rain|storm|cloud| thunder|hurricane|tornado| hail| snow|flood| snow)", re.IGNORECASE)

	#goods = []
	for line in f_src:
		try:
			parsed = json.loads(line)
			text = parsed["text"]
			#coordinates = parsed['retweeted_status']['coordinates']
			coordinates = parsed['coordinates']
			created_at = parsed['created_at']
			#print coordinates
			#print created_at
			#print "AAAA"
			if not coordinates or not created_at:
				#if "coordinates" in line:
				#	#print line
				#	pass
				continue
			else:
				#print coordinates, ":", text, '\n'
				#goods.append(parsed)
				#print line
				#print "created at:", created_at
				timestamp = dateutil.parser.parse(created_at)
				#print "timestamp:", timestamp, "stop_timestamp:", stop_timestamp, "timestamp - start_timestamp:", timestamp - start_timestamp, "stop_timestamp - timestamp:", stop_timestamp - timestamp
				#print coordinates
				if start_timestamp <= timestamp <= stop_timestamp:
					#print "Time HIT!!!!"
					if coordinates["type"] == "Point":
						lon, lat = coordinates["coordinates"]
						#print lat, lon, haversine_dist(geo_center, (lat, lon))
						if haversine_dist(geo_center, (lat, lon)) <= geo_radius:
							print "Geo HIT!!!"
							print parsed
					
		except Exception as e:
			if True:
				print e
			else:
				pass

	f_src.close()


if __name__ == "__main__":
	main()

