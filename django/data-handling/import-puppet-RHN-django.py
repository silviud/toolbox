#!/usr/bin/env python
'''
blurb: Imports hosts from foreman / puppet and overlays redhat satellite data into django models

'''
import sys
import os
import simplejson
import urllib

# My models
from infrastructure.models import Host, DataCenter, Owner, Hardware, HardwareModel
from environments.models import Environment
from applicationserver.models import ApplicationGroup, ApplicationServer, ApplicationInstance

import re
import xml.sax.handler
import urllib

puppetUrl = "http://provision01.jfa:4000/hosts/"
satellite = "http://satellite01.domain.com/rpc/api"

from xmlrpclib import Server
client = Server(satellite)
print "Getting  into RedHat Satellite"
auth = client.auth.login('my username here', 'password here please')
print "Obtaing list of all systems"
systems = client.system.listUserSystems(auth)

def satelliteProbe(hostId):
    '''Makes calls to get details for machine
    '''
    print "Getting host details from Satellite"
    try:
        details = client.system.getNetwork(auth, int(hostId))
        return str(details['hostname']), str(details['ip'])
    except:
        return "Unknown FQDN"
    
def puppetProbe(fqdn):
    print "Getting host details from Puppet"
    url = puppetUrl + fqdn + "/facts?format=json"    
    result = simplejson.load(urllib.urlopen(url))
    return result[fqdn]['environment'], result[fqdn]['productname']

def msg(string):
    print(string)

def addHost(host, env):
    '''Imports the host and environment
    '''
    try:
        h = Host.objects.get(fqdn = host)
        if h.pk:
            msg("Host " + host+ " already exists")
            return h
    except:
        pass
    msg("importing new host " + host)


    # Hardware Model
    try:
        tenv, tmodel = puppetProbe(host)
        try:
            hwm = HardwareModel.objects.get(name = tmodel)
        except:
            hwm = HardwareModel(name = tmodel, power_usage=300, size=1)
            hwm.save()
    except:
        hwm = unknown


    # Machine itself
    t =  classifier.guess(host)
    try:
        print "AI says " + t[0][0]
        dc = DataCenter.objects.get(name = t[0][0])
    except:
        try:
            dc = DataCenter(name=t[0][0])
            dc.save()
        except:
            print "AI Error"
    hw = Hardware(name = "FIXME " + host, hardware_model = hwm)
    hw.save()
    h = Host(fqdn=host, environment=Environment.objects.get(name=env.name), owner=amo, hardware=hw )
    h.save()
    return h
    
'''
Main Code
'''

for system in systems:
    hostname, ip = satelliteProbe(int(system['id']))
    msg("Hostname " + str(hostname) + " IP:" + str(ip))
    msg("Details name:" + str(system['name']) + " last_checkin:" + str(system['last_checkin']))
    h = addHost(hostname, unknownenv)
