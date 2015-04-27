#!/usr/bin/env python
# -*- coding: utf8 -*-

import pickle
import dateutil.parser
import time
import numpy
import matplotlib.pyplot as plt
from numpy.lib.stride_tricks import as_strided as ast
import numpy as np
import math
from nltk.stem.lancaster import LancasterStemmer
from nltk.tokenize import RegexpTokenizer
from collections import defaultdict



#from http://www.johnvinyard.com/blog/?p=268
def sliding_window(a,ws,ss = None,flatten = True):
    '''
    Return a sliding window over a in any number of dimensions
    
    Parameters:
        a  - an n-dimensional numpy array
        ws - an int (a is 1D) or tuple (a is 2D or greater) representing the size 
             of each dimension of the window
        ss - an int (a is 1D) or tuple (a is 2D or greater) representing the 
             amount to slide the window in each dimension. If not specified, it
             defaults to ws.
        flatten - if True, all slices are flattened, otherwise, there is an 
                  extra dimension for each dimension of the input.
    
    Returns
        an array containing each n-dimensional window from a
    '''
    
    if None is ss:
        # ss was not provided. the windows will not overlap in any direction.
        ss = ws
    ws = norm_shape(ws)
    ss = norm_shape(ss)
    
    # convert ws, ss, and a.shape to numpy arrays so that we can do math in every 
    # dimension at once.
    ws = np.array(ws)
    ss = np.array(ss)
    shape = np.array(a.shape)
    
    
    # ensure that ws, ss, and a.shape all have the same number of dimensions
    ls = [len(shape),len(ws),len(ss)]
    if 1 != len(set(ls)):
        raise ValueError(\
        'a.shape, ws and ss must all have the same length. They were %s' % str(ls))
    
    # ensure that ws is smaller than a in every dimension
    if np.any(ws > shape):
        raise ValueError(\
        'ws cannot be larger than a in any dimension.\
 a.shape was %s and ws was %s' % (str(a.shape),str(ws)))
    
    # how many slices will there be in each dimension?
    newshape = norm_shape(((shape - ws) // ss) + 1)
    # the shape of the strided array will be the number of slices in each dimension
    # plus the shape of the window (tuple addition)
    newshape += norm_shape(ws)
    # the strides tuple will be the array's strides multiplied by step size, plus
    # the array's strides (tuple addition)
    newstrides = norm_shape(np.array(a.strides) * ss) + a.strides
    strided = ast(a,shape = newshape,strides = newstrides)
    if not flatten:
        return strided
    
    # Collapse strided so that it has one more dimension than the window.  I.e.,
    # the new array is a flat list of slices.
    meat = len(ws) if ws.shape else 0
    firstdim = (np.product(newshape[:-meat]),) if ws.shape else ()
    dim = firstdim + (newshape[-meat:])
    # remove any dimensions with size 1
    dim = filter(lambda i : i != 1,dim)
    return strided.reshape(dim)



#from http://www.johnvinyard.com/blog/?p=268
def norm_shape(shape):
    '''
    Normalize numpy array shapes so they're always expressed as a tuple, 
    even for one-dimensional shapes.
    
    Parameters
        shape - an int, or a tuple of ints
    
    Returns
        a shape tuple
    '''
    try:
        i = int(shape)
        return (i,)
    except TypeError:
        # shape was not a number
        pass

    try:
        t = tuple(shape)
        return t
    except TypeError:
        # shape was not iterable
        pass
    
    raise TypeError('shape must be an int, or a tuple of ints')




def get_time(tweet):
	created_at = tweet['created_at']

	timestamp = dateutil.parser.parse(created_at)
	unix_timestamp = time.mktime(timestamp.timetuple())

	return timestamp, unix_timestamp

def dict_normalize(dct):
	items = dct.items()
	total_words = sum(n for w, n in items)
	res = defaultdict(int,  ( (w, float(n)/total_words) for w, n in items) )
	return res

def dict_normalize_by(dct, ratio):
	items = dct.items()
	res = defaultdict(int, ( (w, float(n)/ratio) for w, n in items) )
	return res

def main():

	mode = "density"
	# "bourbon_ky_thunderstorm_04_02_2015.pkl"
	files = ["cherokee_ga_thunderstorm_04_02_2015.pkl", "floyd_ga_thunderstorm_04_03_2015.pkl", "phelps_mo_thunderstorm_04_02_2015.pkl", "pulaski_ms_thunderstorm_04_02_2015.pkl", "bath_ky_thunderstorm_04_03_2015.pkl"]

	#files = [files[3]]

	ncols = 3
	nrows = int(math.ceil(len(files)/float(ncols)))
	figure, axes = plt.subplots(nrows, ncols)
	axes = axes.reshape(axes.size)

	if mode == "words":
		diffs = []
	elif mode == "cummulative":
		start_percents = []
	elif mode == "density":
		means_before = []
		means_after = []
		means_within = []
		means_before_and_after = []

	for fname, axis in zip(files, axes):
		f_src = open("../fetched_data/"+fname, "rb")
		data, alert_start, alert_stop, geo_center, geo_radius, start_timestamp, stop_timestamp = pickle.load(f_src)
		f_src.close()

#		if fname == "phelps_mo_thunderstorm_04_02_2015.pkl":
#			data = data[500:]

		print len(data)

		if mode == "density":

			times = numpy.array([utime for _, utime in map(get_time, data)])

			hist, bin_edges = numpy.histogram(times, bins=600, density=True)
			bin_centers = (bin_edges[1:]+bin_edges[:-1])/2


			window_size = 20
			window_step = 1
			hist = numpy.mean(sliding_window(hist, window_size, window_step), axis=1)
			bin_centers = numpy.mean(sliding_window(bin_centers, window_size, window_step), axis=1)


			alert_start_utime = time.mktime(alert_start.timetuple())
			alert_stop_utime = time.mktime(alert_stop.timetuple())

			zipped = zip(bin_centers, hist)
			before = numpy.array( [freq for bin_center, freq in zipped if bin_center < alert_start_utime] )
			after = numpy.array( [freq for bin_center, freq in zipped if bin_center > alert_stop_utime])
			within = numpy.array( [freq for bin_center, freq in zipped if alert_start_utime <= bin_center <= alert_stop_utime])


			mean_before = numpy.mean(before)
			mean_after = numpy.mean(after)
			mean_within = numpy.mean(within)
			mean_before_and_after = numpy.mean( numpy.hstack([before, after]) )

			means_before.append(mean_before)
			means_after.append(mean_after)
			means_within.append(mean_after)
			means_before_and_after.append(mean_before_and_after)


			max_hist = numpy.max(hist)

			print max_hist
			print hist
			print bin_centers

			alert_ys = numpy.linspace(0, max_hist, num=10)
			alert_start_xs = numpy.ones(alert_ys.shape) * alert_start_utime
			alert_stop_xs = numpy.ones(alert_ys.shape) * alert_stop_utime


			axis.plot(bin_centers, hist, color="b")
			axis.plot(alert_start_xs, alert_ys, color="r")
			axis.plot(alert_stop_xs, alert_ys, color="r")
			axis.set_title(fname[:-4])
			axis.set_ylabel("Relative frequency of tweets")
			axis.set_xlabel("Unix timestamp")

		elif mode == "cummulative":
			times = numpy.array([utime for _, utime in map(get_time, data)])
			ntweets = numpy.linspace(1, times.size, times.size)
			#ntweets = numpy.linspace(0, 1, times.size)

			max_ntweets = ntweets[-1]

			alert_ys = numpy.linspace(0, max_ntweets, num=10)
			alert_start_xs = numpy.ones(alert_ys.shape) * time.mktime(alert_start.timetuple())
			alert_stop_xs = numpy.ones(alert_ys.shape) * time.mktime(alert_stop.timetuple())

			time_to_search = (time.mktime(alert_start.timetuple()) + time.mktime(alert_stop.timetuple()))/2.0

			start_percent = numpy.searchsorted(times, time_to_search)/float(times.size)
			print start_percent
			start_percents.append(start_percent)

			axis.plot(times, ntweets, color="b")
			axis.plot(alert_start_xs, alert_ys, color="r")
			axis.plot(alert_stop_xs, alert_ys, color="r")
			axis.set_title(fname[:-4])
			axis.set_ylabel("Total number of tweets")
			axis.set_xlabel("Unix timestamp")
		elif mode == "words":
			word_count_before_alert = defaultdict(int)
			word_count_after_alert = defaultdict(int)
			tokenizer = RegexpTokenizer("\w+")
			stemmer = LancasterStemmer()

			for tweet in data:
				try:
					text = tweet['text']
					created_at = tweet['created_at']
					#print text
					tokens = tokenizer.tokenize(text)
					stems = map(stemmer.stem, tokens)
					#print stems
					timestamp = dateutil.parser.parse(created_at)
					if timestamp <= alert_start:
						word_count = word_count_before_alert
					else:
						word_count = word_count_after_alert
					for word in stems:
						word_count[word] += 1
				except Exception as e:
					print e
					print tweet
			#print sorted(word_count_before_alert.items(), key=lambda x: -x[1])
			#print sorted(word_count_after_alert.items(), key=lambda x: -x[1])
			normalize_mode = "total"
			if normalize_mode == "total":
				items = word_count_before_alert.items() + word_count_after_alert.items()
				total_words = sum(n for w, n in items)
				word_count_before_alert = dict_normalize_by(word_count_before_alert, total_words)
				word_count_after_alert = dict_normalize_by(word_count_after_alert, total_words)
			elif normalize_mode == "self":
				word_count_before_alert = dict_normalize(word_count_before_alert)
				word_count_after_alert = dict_normalize(word_count_after_alert)


			diff = {}
			#print word_count_before_alert
			#print word_count_after_alert
			for key in word_count_after_alert.keys():
				#print diff
				#print word_count_after_alert[key], type(word_count_after_alert)
				#print word_count_before_alert[key], type(word_count_before_alert)
				#print word_count_after_alert[key] - word_count_before_alert[key]
				diff[key] = word_count_after_alert[key] - word_count_before_alert[key]
			#print sorted(diff.items(), key=lambda x: -abs(x[1]))
			diffs.append(diff)
	if mode in ["density", "cummulative"]:
		if mode == "cummulative":
			print "start percetns:", start_percents
			print "mean:", numpy.mean(start_percents)
			print "std:", numpy.std(start_percents)
		elif mode == "density":
			means_before = numpy.array(means_before)
			means_after = numpy.array(means_after)
			means_within = numpy.array(means_within)
			means_before_and_after = numpy.array(means_before_and_after)
			print "means before:", means_before
			print "means after:", means_after
			print "means_within:", means_within
			print "means before and after:", means_before_and_after
			
			print "means_after / means_before:", means_after / means_before
			print "means_after / means_before mean:", numpy.mean(means_after / means_before), "means_after / means_before std:", numpy.std(means_after / means_before)
			print "means_within / means_before_and_after:", means_within / means_before_and_after
			print "means_within / means_before_and_after mean:", numpy.mean(means_within / means_before_and_after), "means_within / means_before_and_after std:", numpy.std(means_within / means_before_and_after)


		plt.show()

	elif mode == "words":
		#print diffs
		all_words = reduce(lambda x, y: x+y, ([word for word, count in diff.items()] for diff in diffs), [])
		intersecting_words = [word for word in all_words if all_words.count(word) == len(diffs)]
		intersecting_words = list(set(intersecting_words))
		#print intersecting_words
		#sorted_changers = sorted( ( (word, sum(diff[word] for diff in diffs)/float(len(diffs))) for word in intersecting_words), key = lambda x: -abs(x[1]) )
		changers = []
		for word in intersecting_words:
			counts = numpy.array([diff[word] for diff in diffs])
			mean = numpy.mean(counts)
			std = numpy.std(counts)
			changers.append( (word, mean, std) )
		sorted_changers = sorted(changers, key = lambda x: -abs(x[1]))
		print sorted_changers


		

if __name__ == "__main__":
	main()

