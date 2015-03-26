#!/usr/bin/env python
# -*- coding: utf8 -*-

import pickle


dumpfile = open("statuses_100000_recent_geocode_snow_100000mi.pkl", "rb")
statuses = pickle.load(dumpfile)
dumpfile.close()

for status in statuses:
	print status
	print status.text
	print [str(tag.text) for tag in status.hashtags]
	print status.created_at
	print "\n\n"
