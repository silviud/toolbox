#!/usr/bin/python
import simplejson
import urllib

QUERY_URL="http://someappserver:9902/myjsonservlet"
result = simplejson.load(urllib.urlopen(QUERY_URL))
print result['myapplication']['system_memory'] # prints out 21026160640.0
