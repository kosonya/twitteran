#!/usr/bin/env python
# -*- coding: utf8 -*-

import json
import pickle
import dateutil.parser
import math
import datetime


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

	alert_start = dateutil.parser.parse("Thu Apr 02 18:17:00 -0400 2015")
	alert_stop = dateutil.parser.parse("Thu Apr 02 18:35:00 -0400 2015")
	geo_center = (38.205586, -84.247523)
	geo_radius = 200

	start_timestamp = alert_start - datetime.timedelta(days=1)
	stop_timestamp = alert_stop + datetime.timedelta(days=1)


	goods = []
	for line in f_src:
		try:
			parsed = json.loads(line)
			text = parsed["text"]
			#coordinates = parsed['retweeted_status']['coordinates']
			coordinates = parsed['coordinates']
			created_at = parsed['created_at']
			if not coordinates or not created_at:

				continue
			else:
				timestamp = dateutil.parser.parse(created_at)
				if start_timestamp <= timestamp <= stop_timestamp:
					if coordinates["type"] == "Point":
						lon, lat = coordinates["coordinates"]
						if haversine_dist(geo_center, (lat, lon)) <= geo_radius:
							print "Geo HIT!!!"
							print parsed	
							goods.append(parsed)
		except Exception as e:
			if True:
				print e
				print line
			else:
				pass

	f_src.close()

	f_dst = open("../fetched_data/bourbon_ky_thunderstorm_04_02_2015.pkl", "wb")
	pickle.dump((goods, alert_start, alert_stop, geo_center, geo_radius, start_timestamp, stop_timestamp), f_dst)
	f_dst.close()


if __name__ == "__main__":
	main()

