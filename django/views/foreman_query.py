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
