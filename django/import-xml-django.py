#!/usr/bin/env python
'''
This example reads a XML file from a web service and converts it into a 
python list object and then imports the list objects into existing django Models

XML example
<?xml version="1.0" encoding="UTF-8"?>
<config
        xmlns="http://www.domain.com/site-config-3.0"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.domain.com/site-config-3.0 http://release.domain.com/configuration/settings/site-config-3.0.xsd">

    <product type="polopoly" name="Cms" version="9.14">
        <domain type="bo" name="cms" portbase="0" user="XXX">
        </domain>
        <env name="ci1">
            <host type="bo" name="ci1punter04.ci1.domain.com"/>
        </env>
    </product>

    <product type="glassfish" name="GFConsole" version="3.0">
        <domain type="fe" name="monitordomain" portbase="19000" user="someuser">
        </domain>
        <env name="si1">
            <host type="fe" name="app-1.domain.com"/>
        </env>
        <env name="prod">
            <host type="fe" name="app-1.domain.com"/>
        </env>
        <env name="stage">
            <host type="fe" name="app-1.domain.com"/>
        </env>
        <env name="dev">
            <host type="fe" name="virt-12.domain.com"/>
        </env>
    </product>

    <product type="glassfish" name="Console" version="3.1">
        <domain type="bo" name="consoledomain" portbase="19000" user="someuser">
        </domain>
        <env name="ci1">
            <host type="bo" name="app03.domain.com"/>
        </env>
        <env name="tool">
            <host type="bo" name="app04.domain.com"/>
        </env>

    </product>
</config>

'''

# Some basic imports
import sys
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
import settings
import simplejson
import re
import xml.sax.handler
import urllib

# My application specific imports
from infrastructure.models import Host, DataCenter, Owner, Hardware, HardwareModel
from environments.models import Environment
from applicationserver.models import ApplicationGroup, ApplicationServer, ApplicationInstance
from infrastructure.models import NetworkPort

# URL
xmlurl = 'http://someurl/foo.xml'

# Test if essential link models exist
try:
    dc = DataCenter.objects.get(name = 'JFA')
    amo = Owner.objects.get(name = 'AMO Infrastructure')
except:
    print("init failed, check DC 'JFA' and owner 'AMO Infrastructure' exists!")
    sys.exit(1)

# Test / Create a unknown hardware type model which is used for unidentified equipment
try:
    unknown = HardwareModel.objects.get(name = 'Unknown')
except:
    unknown = HardwareModel(name = "Unknown", power_usage="300", size="1")
    unknown.save()

# this is the important function for converting XML to list python object
def xml2obj(src):
    """
    A simple function to converts XML data into native Python object.
    """
    non_id_char = re.compile('[^_0-9a-zA-Z]')
    def _name_mangle(name):
        return non_id_char.sub('_', name)

    class DataNode(object):
        def __init__(self):
            self._attrs = {}    # XML attributes and child elements
            self.data = None    # child text data
        def __len__(self):
            # treat single element as a list of 1
            return 1
        def __getitem__(self, key):
            if isinstance(key, basestring):
                return self._attrs.get(key,None)
            else:
                return [self][key]
        def __contains__(self, name):
            return self._attrs.has_key(name)
        def __nonzero__(self):
            return bool(self._attrs or self.data)
        def __getattr__(self, name):
            if name.startswith('__'):
                # need to do this for Python special methods???
                raise AttributeError(name)
            return self._attrs.get(name,None)
        def _add_xml_attr(self, name, value):
            if name in self._attrs:
                # multiple attribute of the same name are represented by a list
                children = self._attrs[name]
                if not isinstance(children, list):
                    children = [children]
                    self._attrs[name] = children
                children.append(value)
            else:
                self._attrs[name] = value
        def __str__(self):
            return self.data or ''
        def __repr__(self):
            items = sorted(self._attrs.items())
            if self.data:
                items.append(('data', self.data))
            return u'{%s}' % ', '.join([u'%s:%s' % (k,repr(v)) for k,v in items])

    class TreeBuilder(xml.sax.handler.ContentHandler):
        def __init__(self):
            self.stack = []
            self.root = DataNode()
            self.current = self.root
            self.text_parts = []
        def startElement(self, name, attrs):
            self.stack.append((self.current, self.text_parts))
            self.current = DataNode()
            self.text_parts = []
            # xml attributes --> python attributes
            for k, v in attrs.items():
                self.current._add_xml_attr(_name_mangle(k), v)
        def endElement(self, name):
            text = ''.join(self.text_parts).strip()
            if text:
                self.current.data = text
            if self.current._attrs:
                obj = self.current
            else:
                # a text only node is simply represented by the string
                obj = text or ''
            self.current, self.text_parts = self.stack.pop()
            self.current._add_xml_attr(_name_mangle(name), obj)
        def characters(self, content):
            self.text_parts.append(content)

    builder = TreeBuilder()
    if isinstance(src,basestring):
        xml.sax.parseString(src, builder)
    else:
        xml.sax.parse(src, builder)
    return builder.root._attrs.values()[0]

# Just for debugging
def msg(string):
    print(string)

# Get the XML and Convert it to list
msg("started up")
opener = urllib.FancyURLopener({})
f = opener.open(xmlurl)
msg("opener initialized")
myXml = f.read()
msg("xml data read from url")
# create my python listified object from XML data
deploydata = xml2obj(myXml)
msg("python-i-fied xml data")

'''
Deploydata is now a python list which can be traversed like
	product = deploydata.product
	domains = product.domain
	env = product.env
and so forth...
'''

# Some functions for checking if objects exists to which to link
def addHost(host, env):
    try:
        h = Host.objects.get(fqdn = host.name)
        if h.pk:
            msg("Host " + host.name + " already exists")
            return h
    except:
        msg("WARNING " + str(host.name) + " please add host")
def addEnv(env): 
    try:
        e = Environment.objects.get(name = env.name)
        if e.pk:
            msg("Env " + env.name + " already exists")
            return e
    except:
        pass
    msg("importing new env " + env.name)
    e = Environment(name = env.name, datacenter=dc)
    e.save()
    return e
def addProduct(product, appsrv): 
    try:
        e = ApplicationGroup.objects.get(name = product.name)
        if e.pk:
            msg("product " + product.name + " already exists")
            return
    except:
        pass
    msg("importing new product " + product.name)
    e = ApplicationGroup(name = product.name, application_server=appsrv )
    e.save()    
def addApplicationServer(product):
    try:
        e = ApplicationServer.objects.get(server_type = product.type, version=product.version)
        if e.pk:
            msg("app server " + product.type +":" + product.version + " already exists")
            return e
    except:
        pass
    msg("importing new appserver " + product.type)
    e = ApplicationServer(name = product.type+product.version, 
                          server_type = product.type,
                          version = product.version)
    e.save()
    return e
def addDomain(domain, product):
    try:
        e = ApplicationInstance.objects.get(name = domain.name)
        if e.pk:
            msg("domain " + domain.name + " already exists")
            return
    except:
        pass
    msg("importing new domain " + domain.name)
    e = ApplicationInstance(name = domain.name, 
                            group=ApplicationGroup.objects.get(name=product.name), 
                            instance_type=domain.type, 
                            server=ApplicationServer.objects.get(server_type=product.type, version=product.version), 
                            portbase=domain.portbase )
    e.save()


# In my use case, I de-link all existing models in django before importing
msg("Clearing Data")
for product in deploydata.product:
    for env in product.env:
        if env.host:
            for host in env.host:
                sys.stdout.write(".")
                sys.stdout.flush()
                try:
                    h = Host.objects.get(fqdn = host.name)
                    h.application_instance.clear()
                    h.application_server.clear()
                    h.environment = None
                except Exception, e:
                    print
                    print("WARNING " + str(host.name) + " reason: " + str(e))
msg("")
msg("Updating DATA")
''' This is where the list object created by xml2obj is processed '''
for product in deploydata.product:
    appsrv = addApplicationServer(product)
    addProduct(product, appsrv)
    for domain in product.domain:
        addDomain(domain, product)
    for env in product.env:
        myenv = addEnv(env)
        if env.host:
            for host in env.host:
                try:
                    h = addHost(host, env)
                    h.environment = myenv
                    sys.stdout.write(".")
                    sys.stdout.flush()
                    h.save()
                    for domain in product.domain:
                        i = ApplicationInstance.objects.get(name=domain.name)
                        h.application_instance.add(i)
                        h.application_server.add(i.server)
                except:
                    print("error with host")
msg("")
# end
