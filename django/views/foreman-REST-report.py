#!/usr/bin/python
'''
blurb: Django view to request data from foreman + puppet
'''
import urllib
from django.shortcuts import render_to_response, get_object_or_404
import simplejson

def puppetReport(request):
    """
    calls foreman / puppet and returns a report via a template
    The use case for this was to combine a infrastructure database's data with
    foreman puppet data for the same hosts and merge it into one big report.
    """
    url = "http://provision01.jfa:4000/hosts/?format=json"
    hosts = simplejson.load(urllib.urlopen(url))
    newhosts_array = []
    c = 0
    for host in hosts:
        c = c + 1
        urlh = "http://provision01.jfa:4000/hosts/" + host + "/facts?format=json"
        os = simplejson.load(urllib.urlopen(urlh))
        try:
            newhosts_array.append(os[host])
        except:
            pass
    return render_to_response('infrastructure/report.html',{'hosts': newhosts_array}, mimetype='application/xhtml+xml')

'''
Contents of report.html

<?xml version="1.0" encoding="UTF-8"?>
<report
        xmlns="http://www.unibet.com/site-config-2.0"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.unibet.com/site-config-2.0 http://release.unibet.com/configuration/settings/site-config-2.0.xsd">
	{% for host in hosts %}
		<host fqdn="{{ host.fqdn }}" >
			<!-- product name {{ host.productname }} {{ host.hardwaremodel }} -->
			<!-- serial number {{ host.serialnumber }} -->
			<!-- operating system {{ host.operatingsystem}} {{ host.lsbdistid }} {{ host.architecture }} {{ host.lsbdistdescription }} -->
			<!-- Installed RAM {{ host.memorysize }} -->
			<!-- kernel version {{ host.kernelversion}} -->
			<!-- processor count {{ host.processorcount }} -->
			<!-- physical processor count {{ host.physicalprocessorcount }} -->
			<!-- processor1 type {{ host.processor1 }} -->
			<!-- ip address {{ host.ipaddress }} -->
			<!-- ip address eth0 {{ host.ipaddress_eth0 }} -->
			<!-- mac address eth0 {{ host.macaddress_eth0 }} -->
			<!-- ip address eth1 {{ host.ipaddress_eth1 }} -->
			<!-- mac address eth1 {{ host.macaddress_eth1 }} -->
			<!-- ip address eth2 {{ host.ipaddress_eth2 }} -->
			<!-- mac address eth2 {{ host.macaddress_eth2 }} -->
			<!-- ip address eth3 {{ host.ipaddress_eth3 }} -->
			<!-- mac address eth3 {{ host.macaddress_eth3 }} -->
			
			
		</host>
	{% endfor %}
</report>

'''
