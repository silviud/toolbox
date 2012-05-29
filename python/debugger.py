#!/usr/bin/python
'''
blurb: debug logging functions which report file, line number and objects in logging statements.

debugger.py
By Kegan Holtzhausen

Example Output:
	WARNING jmx.py:203 damGet() 10.0.6.41:custard:unable to update state in db for attribute 'custard-tps:autenticateTPS'
	WARNING jmx.py:204 damGet()index out of range: 0
	INFO daemon.py:145 main() Querying host: 10.0.6.12
	INFO jmx.py:250 close() Closing DB Session down
	WARNING jmx.py:203 damGet() 10.0.6.42:custard:unable to update state in db for attribute 'custard-tps:autenticateTPS'
	WARNING jmx.py:204 damGet()index out of range: 0
	INFO daemon.py:145 main() Querying host: 10.0.6.33

Example Usage:
	Python 2.7.3rc2 (default, Apr 22 2012, 22:30:17) 
	[GCC 4.6.3] on linux2
	Type "help", "copyright", "credits" or "license" for more information.
		>>> from debugger import debugMsg, warningMsg, infoMsg
		>>> a=[]
		>>> infoMsg("test")
		INFO <stdin>:1 <module>() test
		>>> warningMsg("test",object=a)
		WARNING <stdin>:1 <module>() []:test
'''

import sys
import inspect

# Disable debug level
verbose = False

def debugMsg(msg, **kwargs):
    """Prints msg out if verbose = True.
    :param msg: String to print out
    :param kwargs: Not used, see warningMsg
    """
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

def warningMsg(msg, **kwargs):
    """Prints msg out and can dump objects too
    :param msg: String to print out
    :param kwargs: object=SomeObj will print out the object
    """
    if kwargs:
        for key in kwargs:
            try:
                frm = inspect.stack()[1]
                function = str(frm[3])
                line=str(frm[2])
                modulepath=str(frm[1]).split('/')
                module = str(modulepath.pop())
                sys.stderr.write("WARNING " + module + ":" + line + " " + function + "() "+ str(kwargs[key]) + ":" + str(msg) + "\n")
                debugMsg("WARNING " + module + ":" + line + " " + function + "() "+ str(kwargs[key]) + ":" + str(msg) + "\n")
            except:
                sys.stderr.write("WARNING (unknown) " + str(msg) + "\n")
                debugMsg("WARNING (unknown) " + str(msg) + "\n")
                
    else:
        try:
            frm = inspect.stack()[1]
            function = str(frm[3])
            line=str(frm[2])
            modulepath=str(frm[1]).split('/')
            module = str(modulepath.pop())
            sys.stderr.write("WARNING " + module +":"  + line + " " + function + "()" + str(msg) + "\n")
        except:
            sys.stderr.write("WARNING (unknown)" + str(msg) + "\n")
            
 
def infoMsg(msg):
    """Prints msg out
    :param msg: String to print out
    """
    try:
        frm = inspect.stack()[1]
        function = str(frm[3])
        line=str(frm[2])
        modulepath=str(frm[1]).split('/')
        module = str(modulepath.pop())
        print "INFO " + module + ":" + line + " " + function + "() " + str(msg)
    except:
        print "INFO (unknown)" + str(msg)
