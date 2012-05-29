#!/usr/bin/python
'''
blurb: An example of with some simple classes which can be imported and used as in class-example.py.
'''
import os
import sys

verbose = False
info = False
warn = False

def debugMsg(msg, **kwargs):
	""" debugMsg(string, object=OBJECT)"""
	if verbose != False:
		try:
			object = str(kwargs['object'])
		except KeyError, e:
			object = "unknown"
		except Exception, e:
			print "WA WA WAAA, exception: " + str(e)
		sys.stdout.write("DEBUG: " + str(object) + ": " + str(msg) + "\n")
			

def infoMsg(msg, **kwargs):
	""" infoMsg(string, object=OBJECT)"""
	if info != False:
		sys.stdout.write("INFO:" + str(msg) + "\n")

def warnMsg(msg, **kwargs):
	""" warnMsg(string, object=OBJECT)"""
	if warn != False:
		sys.stdout.write("WARN:" + str(msg) + "\n")


class daSql:
	def __init__(self,url,**kwargs):
		""" main sql object, call with url like mysql://hostname/dbname, username="user", password="password" """
		debugMsg("Initializing daSql")
		self.url = url
		self.kwargs = kwargs
	
	def __del__(self):
		debugMsg("Self deleting", object=self)
		self.close()
		debugMsg("Byeee")
		del self.url
		del self.kwargs

	def connect(self):
		try:
			debugMsg("Connecting to " + str(self.url), object=self)
			debugMsg("username " + str(self.kwargs['username']))
			debugMsg("password " + str(self.kwargs['password']))
			
		except KeyError, e:
			warnMsg("Username / Password missing, please call with username=\"user\", password=\"pass\"")
		except Exception, e:
			warnMsg("Error: " + str(e))

	def close(self):
		debugMsg("Disconnecting from database")
		# disconnect from db...	

