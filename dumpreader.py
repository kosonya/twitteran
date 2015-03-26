#!/usr/bin/env python
# -*- coding: utf8 -*-

import re
import json
import pickle

def main():
	f = open("/mnt/data/twitterdump/sample", "r")
	keywords = re.compile("( rain|storm|cloud| thunder|hurricane|tornado| hail| snow|flood| snow)", re.IGNORECASE)
	pattern = re.compile("coordinates")
	retweeted = re.compile("retweeted_status")
	goods = []
	for line in f:
		try:
			parsed = json.loads(line)
			text = parsed["text"]
			coordinates = parsed['retweeted_status']['coordinates']
			if not coordinates:
				continue
			if keywords.search(text):
				print coordinates, ":", text, '\n'
				goods.append(parsed)
		except Exception as e:
			pass

	f.close()
	f = open("/mnt/data/twitterdump/relevant_tweets_sample", "wb")
	pickle.dump(goods, f)
	f.close()

if __name__ == "__main__":
	main()

