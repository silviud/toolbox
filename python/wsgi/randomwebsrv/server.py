#!/usr/bin/env python
"""
Random WebSrv

Listens on a port and writes posted data to file after hash checking

payload is sent to /random/HASH
server compares HASH and payload's hash,
appends to data file

"""
__author__ = "Kegan Holtzhausen <marzubus@gmail.com>"
__version__ = "$Revision: 1 $"

import sys
import re
from wsgiref.simple_server import make_server, WSGIServer
from SocketServer import ThreadingMixIn
from cgi import escape
import logging as logger
from StringIO import StringIO
import hashlib

# Configure the logger
logger.basicConfig(	level=logger.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger.getLogger('randompuker-server')

# Import settings class OR create settings class
try:
    import settings
except ImportError:
    class settings:
        logger.info('No settings file, defaults apply')
        pass


class ThreadingWSGIServer(ThreadingMixIn, WSGIServer):
    pass


class optionsStore:
    # a simple options class for storing attributes
    pass

options = optionsStore()
options.LISTEN_ADDRESS = getattr(settings, 'LISTEN_ADDRESS', '0.0.0.0')
options.LISTEN_PORT = getattr(settings, 'LISTEN_PORT', 8080)
options.OUTFILE = open(getattr(settings, 'OUTFILE', 'random.data'), 'a')

urls = [
    r'random/(.*)$',
    ]


def process_data_app(environ, start_response):
    # process data on the URL
    args = environ['randomwebsrv.url_args']   # Read args if available, URL portions are found in here.
    if args:
        expected_hash = escape(args[0])
        logger.info('expect hash: %s' % expected_hash)
    method = environ['REQUEST_METHOD']
    if method == 'POST':
        try:
            request_body_size = int(environ['CONTENT_LENGTH'])
            request_body = environ['wsgi.input'].read(request_body_size)
        except (TypeError, ValueError):
            request_body = "0"
        try:
            response_body = str(request_body)
        except Exception, e:
            logger.warning('Some error has occurred: %s' % e)
            response_body = "error"
        status = '200 OK'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)

        binary_data = response_body
        binary_md5 = hashlib.sha224(binary_data).hexdigest()
        logger.info('sha1: %s' % binary_md5)

        if binary_md5 == expected_hash:
            logger.info('writing packet to fs')
            options.OUTFILE.write(binary_data)

        return [binary_md5]
    else:
        stdout = StringIO()
        h = environ.items()
        h.sort()
        for k, v in h:
            print >>stdout, k, '=', repr(v)
        start_response("200 OK", [('Content-Type', 'text/plain')])
        return [stdout.getvalue()]


def random_webserver(environ, start_response):
    path = environ.get('PATH_INFO', '').lstrip('/')
    for regex in urls:
        match = re.search(regex, path)
        if match is not None:
            environ['randomwebsrv.url_args'] = match.groups()
    return process_data_app(environ, start_response)

if __name__ == '__main__':
    """ main starts the websrv """
    httpd = make_server(options.LISTEN_ADDRESS, options.LISTEN_PORT, random_webserver, ThreadingWSGIServer)
    logger.info("Server Starts - %s:%s" % (options.LISTEN_ADDRESS, options.LISTEN_PORT))

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

    httpd.server_close()
    options.OUTFILE.close()
    logger.info("Server Stops - %s:%s" % (options.LISTEN_ADDRESS, options.LISTEN_PORT))
    sys.exit(0)