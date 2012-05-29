#!/usr/bin/python
'''
Here is a simple command line arguments parser setup which I use in all my python scripts.
It uses sys and getopt.

You can use short or long args when calling this script.
Example: ./argsv.py  -h 1.2.3.4 -o apache2 --domain=www.unixunion.org

'''


import sys
import getopt

def debugMsg(msg):
    if verbose == True:
        print "DEBUG: " + str(msg)


def usage():
    print 'argsv.py'
    print 'by Kegan Holtzhausen'
    print
    print 'argsv.py'
    print
    print 'mandatory options:'
    print ' -h|--host= host-to-query eg: "www.foo.com"'
    print ' -o|--object= object-to-query eg: "heapmemory"'
    print ' -d|--domain= domain-to-query eg: "glassfishdomain" or "all"'
    print



def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:h:o:", ["domain=", "host=", "object="])
    except getopt.GetoptError, err:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--host"):
            myhost = arg
            debugMsg('setting host to ' + arg)
        elif opt in ("-o", "--object"):
            object = arg
            debugMsg('setting object to ' + arg)
        elif opt in ("-d", "--domain"):
            domainname = arg
            debugMsg('setting domain to ' + arg)
        else:
            print 'skipping INVALID opt: ' + opt + ' ' + arg

    debugMsg('Doing something with all commandline args')
    # So thats that.... now lets use the commandline args and do something useful...
    sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        usage()
    else:
        # set to True for debugging
        verbose=True
        main()


 
 
