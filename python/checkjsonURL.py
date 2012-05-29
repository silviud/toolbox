#!/usr/bin/python
'''
blurb: Simple JSON Nagios Check which can read JSON data from URL and compare to levels / match strings
'''
import sys
import getopt
import simplejson
import urllib
from nagiosEval import nagiosEval

def usage():
    print 'by Kegan Holtzhausen'
    print
    print 'mandatory options:'
    print ' -u|--url= url-to-query eg: "http://www.foo.com/myJsonGeneratingServlet"'
    print ' -o|--object= object-to-query eg: "Status"'
    print ' and'
    print ' -w|--warning warning level AND -c|--critical critical level'
    print ' OR '
    print ' -m|--match match level'
    print
    print "eg: check_jsonUrl.py -u http://live-app-1:22180/node-monitor -o Status -m ACTIVE"

# forces ints / floats to be just that!
def typer(s):
    """Forces ints into ints and floats into floats.
    :param s: String to force into typed
    """
    try:
        int(s)
        return int(s)
    except ValueError:
        try:
            float(s)
            return float(s)
        except ValueError:
            return str(s)

def main():
    """Main
    """
    w = None
    c = None
    m = None

    try:
        opts, args = getopt.getopt(sys.argv[1:], "u:o:w:c:m:", ["url=", "object=", "warning=", "critical=", "match="])
    except getopt.GetoptError, err:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-u", "--url"):
            QUERY_URL=arg
        elif opt in ("-o", "--object"):
            object = arg
        elif opt in ("-w", "--warning"):
            w = typer(arg)
        elif opt in ("-c", "--critical"):
            c = typer(arg)
        elif opt in ("-m", "--match"):
            m = str(arg)
        else:
            print 'skipping INVALID opt: ' + opt + ' ' + arg

    try:
        result = simplejson.load(urllib.urlopen(QUERY_URL))
    except Exception, e:
        print "Unable connect to host / get value"
        sys.exit(3)
    try:
        resulty = nagiosEval(object=object, value=result[object], warning=w, critical=c, match=m)
        exitcode, statusmsg = resulty.evaluate()
        print statusmsg + "|" + str(object) +":"+ str(result[object])
        sys.exit(exitcode)
    except KeyError, e:
        print "No such key"
        sys.exit(3)
    
if __name__ == "__main__":
    if len(sys.argv) < 6:
        usage()
    else:
        main()
