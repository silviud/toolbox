#!/usr/bin/env python
'''
fab -H hudson.hng args:user=gsfadmin,appserver=app01.jfa,app=marcom,port=13048

'''

import os
import glob
import sys
import time
import hashlib
from fabric.api import run

def uname():
	run('uname -s')

#def args(host=None, app=None, user=None, port=None):
def args(**kwargs):
	appserver = kwargs.get('appserver')# hosts = used internally
	user = kwargs.get('user')
	app = kwargs.get('app')
	port = kwargs.get('port')
	print("Targeting %s as user %s to deploy %s via port %s" % (appserver, user, app, port))
