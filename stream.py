#!/usr/bin/env python
# -*- coding: utf8 -*-

import twitter
import pickle
import tweetstream

CONSUMER_KEY = 'nvHkjbdhV4PI9WrYdpqaSmmT5'
CONSUMER_SECRET ='kNEg2zwBaBNQOug3yaQ5r0r0aqXHrMJdTEUvps9a3byG7bVppK'
OAUTH_TOKEN = '85889667-BNUJlo9r8KeA8CXPwkGm3mPkuBD634bUH8QVyQ2tG'
OAUTH_TOKEN_SECRET = 'nKijMpWwDEHmWD7mIWtMhdtIRc4KQo59MvcnQF5ffsdxJ'

#api = twitter.Api(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, access_token_key=OAUTH_TOKEN, access_token_secret=OAUTH_TOKEN_SECRET) 

#print api.VerifyCredentials()

#statuses = api.GetHomeTimeline()
#for status in statuses:
#	print status.text
#	print "\n\n"

#GetSearch(self, term=None, geocode=None, since_id=None, max_id=None, until=None, count=15, lang=None, locale=None, result_type='mixed', include_entities=None)
#Return twitter search results for a given term.

#36.35,-86.92
#polygon 8mi
#Nashville 30mi
#<onset>2013-09-10T15:31:00-05:00</onset> <expires>2013-09-10T16:00:00-05:00</expires>

#statuses = api.GetSearch(term = "FEMA", count = 100, geocode=("36.350000","-86.920000","3000mi"))

#statuses = api.GetSearch(geocode="36.35,-86.92,3000mi", until="2013-09-11", count = 10)

#statuses = api.GetSearch(until="2013-09-11", count = 10)

#statuses = api.GetSearch(term = "snow", count = 100000, geocode=("45.023513", "-109.915807", "100mi"), result_type="recent")

#print statuses

#dumpfile = open("statuses_100000_recent_geocode_snow.pkl", "wb")
#pickle.dump(statuses, dumpfile)
#dumpfile.close()

#for status in statuses:
#	print status.text
#	print "\n\n"

stream = tweetstream.SampleStream("hipno.zomby@gmail.com", "karidola")
for tweet in stream:
	print tweet
