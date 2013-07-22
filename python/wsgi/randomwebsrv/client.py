#!/usr/bin/env python
"""
RandomPuker Agent,

Posts data from /dev/random or /dev/urandom in chunks
to the Random WebSrv, along with the hash of the payload.

"""

import sys
import threading
import urllib2
import hashlib
import time
import logging as logger

# Configure the logger
logger.getLogger('randompuker-agent')
logger.basicConfig(	level=logger.INFO, format='%(asctime)s %(levelname)s %(message)s')

url = 'http://someserver:8080/random'
source_random = '/dev/random'
payload_size = 16384
read_size = 128


class RandomPuker(threading.Thread):
    """ posts chunks of data from /dev/random to a web service """
    bytes = ""

    def __init__(self):
        super(RandomPuker, self).__init__()
        logger.info('%s gathering data, please wait' % self)
        self._stop = threading.Event()

    def run(self):
        while True:
            if self.stopped():
                logger.info('stopping')
                self._Thread__stop()
                sys.exit(0)

            else:
                if self.readbytes() >= payload_size:
                    hash = hashlib.sha224(self.bytes).hexdigest()
                    req = urllib2.Request('%s/%s' % (url, hash), self.bytes, {'Content-Type': 'application/octet-stream'})
                    self.bytes = ""
                    try:
                        sys.stdout.write('.')
                        sys.stdout.flush()
                        result = urllib2.urlopen(req)
                        response_hash = result.read()
                    except:
                        logger.warning('error sending data, sleeping')
                        time.sleep(5)

    def readbytes(self):
        with open(source_random, 'rb') as f:
            self.bytes += f.read(read_size)
        time.sleep(0.2)
        return len(self.bytes)

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

if __name__ == '__main__':
    agents = [RandomPuker()]
    for agent in agents:
        agent.start()
        agent.join()

    while True:
        try:
            for agent in agents:
                if agent.stopped():
                        logger.info('agent shutting down')
                        time.sleep(1)
            time.sleep(0.2)
        except KeyboardInterrupt:
            logger.info('killing threads')
            for agent in agents:
                logger.info('killing agent %s' % agent)
                agent.stop()
                agent.join()
                logger.info('removing agent')
            logger.info('exit')
            sys.exit(0)