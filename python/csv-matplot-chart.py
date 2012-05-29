#!/usr/bin/env python
'''
blurb: Plotting multiple values from CSV-like data onto matplotlib graphs
requires: matplotlib, numpy
'''
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
from matplotlib.ticker import EngFormatter

bigy = 0
smally = 0

print("Reading in logfile")

'''
 First lets sanatize the log file since there are sometimes concats happening which fuck shit up.
 Data format:
	ms_uptime, q, q, q, q, yaw, pitch, roll, accel_X, accel_Y, accel_Z, gyro_X gyro_Y, gyro_Z, magn_X, magn_Y, magn_Z, 0, g_X, g_Y, g_Z, sampletime
	8091,A2303A3E,903E44BF,CA521DBF,AB9814BC,0.00,0.00,0.00,19.00,-20.00,15.00,-6.61,2.78,-0.83,-16.58,-25.97,-526.00,0.00,0.56,-0.59,0.44,37
'''

dirty = open('/tmp/LOG00223.TXT')
regex = re.compile(r"^\d{4,},(\w{8},){4}([-]?\d+\.\d+,){16}\d{2,}.*$")
header = "ms_uptime, q, q, q, q, yaw, pitch, roll, accel_X, accel_Y, accel_Z, gyro_X, gyro_Y, gyro_Z, magn_X, magn_Y, magn_Z, zero, g_X, g_Y, g_Z, sampletime\r\n"

print("Writing new log file")
tmp = open('/tmp/foop.log','w')
tmp.write(header)

for line in dirty:
	m = regex.match(line);
	if m:
		tmp.write(m.group() + "\r\n")
	else:
		print("Bad line: " + line)

print("Opening newly cleaned log")
csvfile = file('/tmp/foop.log')
print("Plotting data")
r = matplotlib.mlab.csv2rec(csvfile, comments='#', skiprows=0, checkrows=0, delimiter=',', converterd=None, names=None, missing='', missingd=None, use_mrecords=False)
	
print("Creating chart root")
formatter = EngFormatter(unit='G', places=1)
timeformat = EngFormatter(unit='ms', places=1)

fig = plt.figure()
ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
ax.set_xlabel('x data')
ax.set_ylabel('y data')

# calibrate graph scale to magnitude
print("Resizing the matter stream")
for tmp in r.g_x:
	if tmp > bigy:
		bigy = tmp + 1
	if tmp < smally:
		smally = tmp - 1

ax.set_ylim(-6.0,+6.0)
print("Plotting")
ax.plot(r.ms_uptime,r.g_x, color='blue', lw=1)
ax.plot(r.ms_uptime,r.g_y, color='red', lw=1)
ax.plot(r.ms_uptime,r.g_z, color='green', lw=1)
ax.xaxis.set_major_formatter(timeformat)
ax.yaxis.set_major_formatter(formatter)
plt.show()
fig.savefig('test.png')

