#!/usr/bin/python
'''
blurb: View that takes django objects and templates them into XML
'''

from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.cache import cache_page

# Model imports
from applicationserver.models import ApplicationServer, ApplicationInstance, ApplicationGroup
from environments.models import Environment, EnvApplicationServerProp

@cache_page(900)
def globalXML(request):
    """
    Returns a XML Deployment Plan of all applications, caches page for 15 minutes
    
    **Template:**
    
    :template: `deploymentMap.html`
    
    """
    environments = Environment.objects.select_related()
    products = ApplicationGroup.objects.select_related()
    print("Done Getting objects, lets render")
    return render_to_response('infrastructure/deploymentMap.html',{'products': products, 'environments': environments}, mimetype='application/xhtml+xml')


'''
Contents of deploymentMap.html

<?xml version="1.0" encoding="UTF-8"?>
<config
        xmlns="http://www.unibet.com/site-config-2.0"
        xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        xsi:schemaLocation="http://www.unibet.com/site-config-2.0 http://release.unibet.com/configuration/settings/site-config-2.0.xsd">
   {% for product in products %}
      <product type="{{product.application_server.server_type}}" name="{{product.name}}" version="{{product.application_server.version}}">
         {% for instance in product.applicationinstance_set.all %}
            <domain type="{{instance.instance_type}}" name="{{instance.name}}" portbase="{{instance.portbase}}" user="admin"></domain>
            {% for environment in environments %}
               <env name="{{environment.name}}">
               {% for host in instance.host_set.all %}
                  {% if host.environment = environment %}<host type="{{instance.instance_type}}" name="{{host.fqdn}}"/>{% endif %}
               {% endfor %}
               </env>
            {% endfor %}
         {% endfor %}
      </product>
   {% endfor %}
</config>

'''
