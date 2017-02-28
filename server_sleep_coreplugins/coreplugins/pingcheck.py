#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import configparser
import subprocess

import logging
from server_sleep_api import PluginInterface


class pingcheck(PluginInterface.AbstractCheckPlugin):
    """
check for computers in your network which are running
    """

    def __init__(self):
        # Read Configfile
        config = configparser.ConfigParser()
        config.read('../serversleep/checkmodules/pingcheck.cfg')
        self.hostlist = eval(config.get('pingcheck', 'hostlist'), {}, {})
        self.max_hosts = int(config.get('pingcheck', 'max_hosts'))
        self.logger = logging.getLogger(__name__)

    def __del__(self):
        pass

    def check(self):
        try:
            count = 0;
            for host in self.hostlist:
                ret = subprocess.call("ping -c 2 %s" % host,
                                      shell=True,
                                      stdout=open('/dev/null', 'w'),
                                      stderr=subprocess.STDOUT
                                      )
                if ret == 0:
                    self.logger.info("Pingcheck: Host " + host + " is up!")
                    count += 1
                    if count > self.max_hosts:
                        self.logger.info("Pingcheck: Not Ready for sleep! More hosts active then allowed!")
                        return 1
                else:
                    self.logger.info("Pingcheck: Host " + host + " is down!")

            self.logger.info("Pingcheck: Ready for sleep!")
            return 0
        except:
            return -1

    @staticmethod
    def run():
        logger = logging.getLogger(__name__)
        instance = pingcheck()
        logger.info("Pingcheck: check started")
        return instance.check()

    @staticmethod
    def configure():
        configurable = []
        configurable.append(
            ["pingcheck", "hostlist", '("hostname","192.168.0.1")', "list of ip-addresses or hostnames to check"])
        configurable.append(["pingcheck", "max_hosts", '0',
                             "maximal amount of network devices allowed for putting the machine to sleep"])
        return configurable

    def sleep(self):
        pass

    def wake(self):
        pass

# for testing purpose
if __name__ == '__main__':
    os.chdir('../')
    print(pingcheck.run())
    print(pingcheck.configure())
    print(pingcheck.__doc__)
