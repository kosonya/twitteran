#!/usr/bin/env python
# -*- coding: utf8 -*-

import pickle
import dateutil.parser
import time
import numpy

import numpy as np
import math
from nltk.stem.lancaster import LancasterStemmer
from nltk.tokenize import RegexpTokenizer
from collections import defaultdict

from mdp.nodes import KMeansClassifier

def main():

	files = ["cherokee_ga_thunderstorm_04_02_2015.pkl", "floyd_ga_thunderstorm_04_03_2015.pkl", "phelps_mo_thunderstorm_04_02_2015.pkl", "pulaski_ms_thunderstorm_04_02_2015.pkl", "bath_ky_thunderstorm_04_03_2015.pkl"]

	tweets = []


	nclusters = 5

	for fname in files:
		f_src = open("../fetched_data/"+fname, "rb")
		print "Loading", "../fetched_data/"+fname
		data, alert_start, alert_stop, geo_center, geo_radius, start_timestamp, stop_timestamp = pickle.load(f_src)
		f_src.close()
		tweets += data
		print "Done loading!"

	
	tokenizer = RegexpTokenizer("\w+")
	stemmer = LancasterStemmer()

	stems = defaultdict(int)

	stemmed_tweets = []


	print "Tokenizin, stemmin, buildin dict n stuff"

	for tweet in tweets:
		try:
			text = tweet['text']
			tweet_tokens = tokenizer.tokenize(text)
			tweet_stems = map(stemmer.stem, tweet_tokens)
			
			stemmed_tweets.append(tweet_stems)

			for stem in tweet_stems:
				stems[stem] += 1

		except Exception as e:
			print e
			print tweet


	print "Done!"
	stems_lst = [stem for stem in sorted(stems.items(), key=lambda x: -x[1]) if stem[1] > 10]
	print stems_lst
	print len(stems_lst)


	feature_matrix = numpy.zeros([len(stemmed_tweets), len(stems_lst)])

	print feature_matrix.shape, feature_matrix.size

	print "Building feature matrix"


	for nrow in xrange(len(stemmed_tweets)):
		for ncol in xrange(len(stems_lst)):
			stem, freq = stems_lst[ncol]
			tweet_stems = stemmed_tweets[nrow]
			feature_matrix[nrow][ncol] = tweet_stems.count(stem)

	print "Feature matrix built"

	print feature_matrix

	knode = KMeansClassifier(nclusters)

	print "Training node"
	knode.train(feature_matrix)
	print "Training done"

	print "Stopping training"
	knode.stop_training()
	print "Training stopped"


	f_dst = open("cluster_data_n%d.pkl" % nclusters, "wb")
	pickle.dump((knode, tokenizer, stemmer, stems_lst, nclusters), f_dst)
	f_dst.close()	

	return

	


		

if __name__ == "__main__":
	main()

