#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import configparser
import subprocess

from serversleep.log import log
from server_sleep_api import PluginInterface

class pyloadcheck(PluginInterface.AbstractCheckPlugin):
    """
check if pyLoad is currently downloading
    """

    def __init__(self):
        # Read Configfile
        config = configparser.ConfigParser()
        config.read('../serversleep/checkmodules/pyloadcheck.cfg')
        self.path = str(config.get('pyloadcheck', 'path'))
        self.logger = log()

    def __del__(self):
        pass

    def check(self):
        try:
            CheckExprs = ("No downloads running", "Could not establish connection")

            cmd = "pyLoadCli status"
            ps = subprocess.Popen(path + cmd, shell=True, stdout=subprocess.PIPE)

            output = ps.stdout.read()
            ps.stdout.close()
            ps.wait()
            for Expr in CheckExprs:
                if (re.match(CheckString, output)):
                    self.log("pyLoadCheck: Ready for sleep! PyLoad is idle.")
                    return 0

            self.log("pyLoadCheck: Not Ready for sleep! PyLoad is working.")
            return 1
        except:
            return -1

    @staticmethod
    def run():
        instance = pyloadcheck()
        instance.logger.log("pyLoad Check: check started")
        return instance.check()

    @staticmethod
    def configure():
        configurable = []
        configurable.append(["pyloadcheck", "path", "/usr/bin/", "path where the pyLoad binaries are stored"])
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
