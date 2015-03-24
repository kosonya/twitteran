#!/usr/bin/env python
# -*- coding: utf8 -*-

import twitter

CONSUMER_KEY = 'nvHkjbdhV4PI9WrYdpqaSmmT5'
CONSUMER_SECRET ='kNEg2zwBaBNQOug3yaQ5r0r0aqXHrMJdTEUvps9a3byG7bVppK'
OAUTH_TOKEN = '85889667-BNUJlo9r8KeA8CXPwkGm3mPkuBD634bUH8QVyQ2tG'
OAUTH_TOKEN_SECRET = 'nKijMpWwDEHmWD7mIWtMhdtIRc4KQo59MvcnQF5ffsdxJ'

api = twitter.Api(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, access_token_key=OAUTH_TOKEN, access_token_secret=OAUTH_TOKEN_SECRET) 

print api.VerifyCredentials()

statuses = api.GetHomeTimeline()
for status in statuses:
	print status.text
	print "\n\n"

#GetSearch(self, term=None, geocode=None, since_id=None, max_id=None, until=None, count=15, lang=None, locale=None, result_type='mixed', include_entities=None)
#Return twitter search results for a given term.

statuses = api.GetSearch(term = "FEMA", count = 100)
for status in statuses:
	print status.text
	print "\n\n"
