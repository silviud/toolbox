#!/bin/python
'''
as a part of my globals.py

Here is a useful stack examination combo, I use this to print out line numbers from where my functions are calling debugMsg.

This code provides:
	python file name
	line number
	python function calling
	message

Example Output:
	WARNING jmx.py:203 damGet() 10.0.6.41:custard:unable to update state in db for attribute 'custard-tps:autenticateTPS'
	WARNING jmx.py:204 damGet()index out of range: 0
	INFO daemon.py:145 main() Querying host: 10.0.6.12
	INFO jmx.py:250 close() Closing DB Session down
	WARNING jmx.py:203 damGet() 10.0.6.42:custard:unable to update state in db for attribute 'custard-tps:autenticateTPS'
	WARNING jmx.py:204 damGet()index out of range: 0
	INFO daemon.py:145 main() Querying host: 10.0.6.33

Example Usage:
from globals import debugMsg
debugMsg("setting result to attrNone")
'''

import sys
import inspect

verbose = False

def debugMsg(msg):
    if verbose == True:
        try:
            frm = inspect.stack()[1]
            function = str(frm[3])
            line=str(frm[2])
            modulepath=str(frm[1]).split('/')
            module = str(modulepath.pop())
            print "DEBUG " + module + ":"  + line + " " + function + "()" + str(msg)
        except:
            print "DEBUG (unknown) " + str(msg)
