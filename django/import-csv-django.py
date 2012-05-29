#!/usr/bin/env python
'''
This example shows how to import CSV data and link with other django models.
this reads the file Hardware-new.csv and creates models accordingly!

My CSV structure:
	Hardware,Location,FQDN,rackname,ManagementIP,HW Model,SerialNumber
	ubhw-0001,KWK,kwkbo03.kwk.mydomain.com,S-909,10.22.17.31,Sun Microsystems Sun Fire X4100 M2,1321321321
	ubhw-0002,KWK,kwkbo04.kwk.mydomain.com,S-906,10.22.17.32,Sun Microsystems Sun Fire X4100 M2,43214324342
	ubhw-0003,KWK,kwkbo05.kwk.mydomain.com,S-909,10.22.17.33,Sun Microsystems Sun Fire X4100 M2,43242314231
	ubhw-0004,KWK,kwkbo06.kwk.mydomain.com,S-908,10.22.17.34,Sun Microsystems Sun Fire X4100 M2,43214324121

This is a very specific example ripped out from a inventory database prototype. But it illustrates
how to import models from csv and check for duplicate and link to other objects.

This script lies in the top level django application directory along side settings.py and my applications
so it has import access to `appname`.models

'''
# some basic imports
import sys
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import settings
import simplejson
import urllib
import csv

# my django application specific models to import, you would put your own here.
from infrastructure.models import Host, DataCenter, Owner, Hardware, HardwareModel, Rack
from environments.models import Environment
from applicationserver.models import ApplicationGroup, ApplicationServer, ApplicationInstance

# just a debug statement
def msg(string):
    print(string)

msg("Test / Create default product owner AMO Infrastructure")
try:
    amo = Owner.objects.get(name = 'AMO Infrastructure')
except:
    amo = Owner(name='AMO Infrastructure')
    amo.save()

msg("Opening CSV")
# open the specific CSV. you should getopt this.
f = open('./Hardware.csv', 'r')
msg("Reading ...")
reader = csv.reader(f)
msg("Starting Import")
for line in reader:
    msg(" importing " + line[0])
    name = line[0]
    location = line[1]
    fqdn = line[2]
    rack = line[3]
    ilo = line[4] 
    model = line[5]
    serial = line[6]

    # Test / Create Hardware Object
    try:
        hw = HardwareModel.objects.get(name = model) 
    except:
        hw = HardwareModel(name = model, power_usage="300", size="1")
        hw.save()

    # Test / Create Datacenter Object
    try:
        dc = DataCenter.objects.get(name = location)
    except:
        dc = DataCenter(name=location)
        dc.save()

    # Test / Create Rack Object
    try:
        rack = Rack.objects.get(name = rack)
    except:
        rack = Rack(name = rack, datacenter = dc, size=42)
        rack.save()

    # Check if machine already exists | create
    try:
        machine = Hardware.objects.get(name = name)
        msg("Machine found! attempting to add host " + str(fqdn))
        try:
            host = Host(fqdn = fqdn, hardware = machine)
            host.save()
            msg("Host successfully created")
        except Exception, e:
            msg("Error with host " + str(fqdn) + " reason " + str(e))
    except:
        try:
            machine = Hardware(name = name, hardware_model = hw, rack = rack, owner = amo, serial_number = serial, ilo_address = ilo ) 
            machine.save()
            msg("Machine successfully created, adding host " + str(fqdn))
            host = Host(fqdn = fqdn, hardware = machine)
            host.save()
            msg("Host successfully created")
        except Exception, e:
            msg("Error with machine/host " + str(fqdn) + " reason " + str(e))

# end
