#!/usr/bin/env python
"""
Convert CSV Data into Numpy and sort n report
"""

import getopt
import math
import random
import datetime
import numpy as np
import re
import sys
import csv

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.mlab as mlab
import matplotlib.cbook as cbook
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.ticker import EngFormatter
from matplotlib.dates import AutoDateFormatter, AutoDateLocator



def readData():
	print("Appdynamics Worst Performers")
	csvfile = file('output.txt')
	r = matplotlib.mlab.csv2rec(csvfile, comments='#', skiprows=0, checkrows=0, delimiter=',', converterd=None, names=None, missing='', missingd=None, use_mrecords=False)
	return r


if __name__ == "__main__":
	'''
 dtype=[('id', '<i8'), ('name', '|S55'), ('original_name', '|S55'), ('service_levels', '|S8'), ('end_user_time_ms', '|O8'), ('page_render_time_ms', '|O8'), ('network_time_ms', '|O8'), ('server_time_ms', '<i8'), ('max_server_time_ms', '<i8'), ('min_server_time_ms', '<i8'), ('calls', '|S10'), ('calls__min', '|S5'), ('errors', '|S7'), ('error_', '<f8'), ('slow_requests', '|S6'), ('very_slow_requests', '|S7'), ('stalled_requests', '|S6'), ('cpu_used_ms', '|O8'), ('block_time_ms', '|O8'), ('wait_time_ms', '|O8'), ('tier', '|S17'), ('type', '|S11')])
	'''
	print("Starting")
	r=readData()
	nsorted = np.lexsort((r.calls, r.slow_requests, r.very_slow_requests, r.stalled_requests))
	print
	print("Worst by Slow and Very Slow reqs")
	print("================================")
	x = 1
	while x < 11:
		t = list(r[nsorted[nsorted.size-x]])
		print('Number %s: Transaction: %s Tier %s with Slow count of %s and Very slow count of %s and Stall count of %s out of %s Calls' % (x,t[1], t[20], t[14], t[15], t[16], t[10]))
		x=x+1

	nsorted = np.lexsort((r.calls,r.server_time_ms))
	print
	print("Worst by Server Time")
	print("================================")
	x = 1
	while x < 11:
		t = list(r[nsorted[nsorted.size-x]])
		print('Number %s: Transaction: %s Tier %s with Server Time of %s' % (x,t[1], t[20], t[7]))
		x=x+1

	nsorted = np.lexsort((r.calls,r.error_))
	print
	print("Highest Error Percentage Rate")
	print("================================")
	x = 1
	while x < 11:
		t = list(r[nsorted[nsorted.size-x]])
		print('Number %s: Transaction: %s Tier %s with Error Rate of %s Percent out of %s transactions' % (x,t[1], t[20], t[13], t[10]))
		x=x+1

