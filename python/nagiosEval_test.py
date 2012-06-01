#!/usr/bin/python
from nagiosEval import nagiosEval

w = int(50)
c = int(100)
m = None
values = [10, 75, 105]

for value in values:
	print 'Examining value %s' % (value)
	result = nagiosEval(value=value, warning=w, critical=c, match=m)
	exitcode, statusmsg = result.evaluate()
	print 'Exit code: %s, status %s' % ( exitcode, statusmsg )

# swapp crit and warning around for checking where lower = bad
c = int(50)
w = int(100)
m = None
values = [105, 75, 10]
for value in values:
   print 'Examining value %s' % (value)
   result = nagiosEval(value=value, warning=w, critical=c, match=m)
   exitcode, statusmsg = result.evaluate()
   print 'Exit code: %s, status %s' % ( exitcode, statusmsg )


# now test MATCH which makes sure that a the output is a specific value
c = None
w = None
m = "Fwoop"
values = [1.05, 10, 'wew', 'Fwoop']
for value in values:
   print 'Examining value %s' % (value)
   result = nagiosEval(value=value, warning=w, critical=c, match=m)
   exitcode, statusmsg = result.evaluate()
   print 'Exit code: %s, status %s' % ( exitcode, statusmsg )
