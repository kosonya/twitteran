#!/usr/bin/env python
# -*- coding: utf8 -*-

import json

def main():
	f_src = open("/home/maxikov/Dropbox/cmu/advanced_machine_learning/twitterdump/dump_mar_31_9_10", "r")
	f_dst = open("../twitterdump/dump_mar_31_9_10_with_geo", "w")
	for line in f_src:
		try:
			parsed = json.loads(line)
			geo = parsed.get('geo', None)
			coordinates = parsed.get('coordinates', None)
			rt = parsed.get('retweeted_status', None)
			if rt:
				rt_coordinates = rt.get('coordinates', None)
				rt_geo = rt.get('geo', None)
			else:
				rt_coordinate = None
				rt_geo = None

			if coordinates or geo or rt_coordinates or rt_geo:
				print line
				f_dst.write(line)
		except Exception as e:
			print e

	f_src.close()
	f_dst.close()

if __name__ == "__main__":
	main()

