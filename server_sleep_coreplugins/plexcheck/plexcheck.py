#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, signal, subprocess, re, datetime
import configparser
from serversleep.log import log
from server_sleep_api import PluginInterface

class plexcheck(PluginInterface.AbstractCheckPlugin):
    """
Check if Plex had any connections or streams in a configurable time
    """

    def __init__(self):
        # Read Configfile
        config = configparser.ConfigParser()
        config.read('../serversleep/checkmodules/plexcheck.cfg')

        # add your options here like this:
        self.conf_idletime = int(config.get('plexcheck', 'idletime'))
        self.conf_logfile = config.get('plexcheck', 'logfile')
        self.conf_format = config.get('plexcheck', 'timeformat')
        self.logger = log()

    def __del__(self):
        pass

    def check(self):
        # try:
        cmd = "tail -n 1 "

        last_log = os.popen(cmd + self.conf_logfile).read()

        fields = last_log.split()

        datestr = fields[0] + " " + fields[1] + " " + fields[2] + " " + fields[3]

        date = datetime.datetime.strptime(datestr, self.conf_format)
        date_now = datetime.datetime.now()

        date_idletime = datetime.timedelta(seconds=self.conf_idletime)

        if (date_now - date > date_idletime):
            self.logger.log("Plexcheck: Ready for sleep!")
            return 0

        self.logger.log("Plexcheck: Not ready for sleep!")
        return 1

    # except:
    #	self.logger.log("Plexcheck: An unexpected error occured!", 1)
    #	return -1

    @staticmethod
    def run():
        instance = plexcheck()
        instance.logger.log("Plexcheck: check started")
        return instance.check()

    @staticmethod
    def configure():
        configurable = []
        # add the configfile option you used here also
        # configurable.append([sectionname, optionname, defaultvalue, description])
        configurable.append(["plexcheck", "logfile",
                             '/var/lib/plexmediaserver/Library/Application Support/Plex Media Server/Logs/Plex Media Server.log',
                             "Plex Logfile to analyse"])
        configurable.append(["plexcheck", "idletime", '3600', "Time plex has to be idle for shutdown (in seconds)"])
        configurable.append(["plexcheck", "timeformat", '%b %d, %Y %H:%M:%S', "Time format plex uses in logfile"])
        return configurable

    def sleep(self):
        pass

    def wake(self):
        pass

# for testing purpose
# if you run "python example.py" the important functions will be executed
if __name__ == '__main__':
    os.chdir('../')
    print(plexcheck.run())
    print(plexcheck.configure())
    print(plexcheck.__doc__)
