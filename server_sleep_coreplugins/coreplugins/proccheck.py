#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, signal, subprocess, re
import configparser
import logging
from server_sleep_api import PluginInterface

class proccheck(PluginInterface.AbstractCheckPlugin):
    """
Write what your check do here!
    """

    def __init__(self):
        # Read Configfile
        config = configparser.ConfigParser()
        config.read('../serversleep/checkmodules/proccheck.cfg')

        # add your options here like this:
        self.procs = eval(config.get('proccheck', 'procs'), {}, {})

        self.logger = logging.getLogger(__name__)

    def __del__(self):
        pass

    def check(self):
        try:
            s = subprocess.Popen(["ps", "axw"], stdout=subprocess.PIPE)
            for process in s.stdout:
                for proc in self.procs:
                    pass
                    if re.search(proc, process):
                        self.logger.info("Proccheck: Process found '" + proc + "'!")
                        self.logger.info("Proccheck: Not ready for sleep!")
                        return 1

            self.logger.info("Proccheck: Ready for sleep!")
            return 0
        except:
            self.logger.error("Proccheck: An unexpected error occured!", 1)
            return -1

    @staticmethod
    def run():
        instance = proccheck()
        instance.logger.info("Proccheck: check started")
        return instance.check()

    @staticmethod
    def configure():
        configurable = []
        # add the configfile option you used here also
        # configurable.append([sectionname, optionname, defaultvalue, description])
        configurable.append(["proccheck", "procs", '0', "Regular Expressions for the processes to check for"])
        return configurable

    def sleep(self):
        pass

    def wake(self):
        pass

# for testing purpose
# if you run "python example.py" the important functions will be executed
if __name__ == '__main__':
    os.chdir('../')
    print(proccheck.run())
    print(proccheck.configure())
    print(proccheck.__doc__)
