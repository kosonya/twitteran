#!/usr/bin/env python
# -*- coding: utf8 -*-

import re
import json

def main():
	f = open("/mnt/data/twitterdump/sample", "r")
	keywords = re.compile("( rain|storm|cloud| thunder|hurricane|tornado| hail| snow|flood| snow| shower)", re.IGNORECASE)
	pattern = re.compile("coordinates")
	retweeted = re.compile("retweeted_status")
	for line in f:
		try:
			parsed = json.loads(line)
			text = parsed["text"]
			coordinates = parsed['retweeted_status']['coordinates']
			if not coordinates:
				continue
			if keywords.search(text):
				print coordinates, ":", text, '\n'
		except Exception as e:
			pass

	f.close()

if __name__ == "__main__":
	main()

