#!/usr/bin/python
import urllib2
import base64
basicauth = base64.encodestring('%s:%s' % ('someusername','somepassword'))[:-1] 
req = urllib2.Request("http://foreman.mydomain.com/hosts/")
req.add_header("Authorization", "Basic %s" % basicauth)
req.add_header('Content_Type','application/json')
req.add_header( 'Accept' , 'application/json')
response = urllib2.urlopen(req)
response.read()
