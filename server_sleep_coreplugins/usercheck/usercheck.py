#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, re
import subprocess
import configparser

from serversleep.log import log
from server_sleep_api import PluginInterface

class usercheck(PluginInterface.AbstractCheckPlugin):
    """
check for users which are logged in
    """

    def __init__(self):
        # Read Configfile
        config = configparser.ConfigParser()
        config.read('../serversleep/checkmodules/usercheck.cfg')
        self.max_usr = int(config.get('usercheck', 'max_usr'))
        self.max_usr_local = int(config.get('usercheck', 'max_usr_local'))
        self.max_usr_remote = int(config.get('usercheck', 'max_usr_remote'))
        self.idle_timeout = int(config.get('usercheck', 'idle_timeout'))
        self.logger = log()

    def __del__(self):
        pass

    def check(self):
        try:
            cmd = "w -hs"

            ps = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)

            output = ps.stdout.read()
            ps.stdout.close()
            ps.wait()

            user = 0
            local_user = 0
            remote_user = 0

            i = 0
            for line in output.split("\n"):

                if (line != "" and line != None):
                    self.logger.log("Proccessing User " + str(i))
                    fields = line.split()

                    if (len(fields) < 5):
                        idle = fields[2]
                        location = ":--"
                    else:
                        idle = fields[3]
                        location = fields[2]

                    idle_time = 0
                    hours = 0
                    minutes = 0
                    seconds = 0

                    if (re.match("^[0-9]+\:[0-9]+m$", idle)):
                        # hours:minutes
                        idle = idle.split(":")
                        hours = int(idle[0])
                        minutes = int(idle[1].replace("m", ""))

                    elif (re.match("^[0-9]+\.[0-9]+s$", idle)):
                        # second.microsecond
                        idle = idle.split(".")
                        seconds = int(idle[0])

                    elif (re.match("^[0-9]+\:[0-9]+$", idle)):
                        # minutes:seconds
                        idle = idle.split(":")
                        minutes = int(idle[0])
                        seconds = int(idle[1])
                    else:
                        self.logger.log("User " + str(i) + " Idle time couldn't be parsed!", 2)

                    idle_time = (hours * 60 + minutes) * 60 + seconds
                    self.logger.log("User " + str(i) + " Idle Time = " + str(idle_time) + " secs")
                    local = False

                    if (re.match("^\:.*$", location)):
                        local = True

                    if (idle_time < self.idle_timeout or self.idle_timeout < 0):
                        user += 1
                        if (local):
                            self.logger.log("User " + str(i) + " Location: Local")
                            local_user += 1
                        else:
                            self.logger.log("User " + str(i) + " Location: Remote")
                            remote_user += 1
                    i += 1

            self.logger.log("Users: " + str(i))
            self.logger.log("Active: " + str(user))
            self.logger.log("Inactive: " + str(i - user))
            self.logger.log("Local: " + str(local_user))
            self.logger.log("Remote: " + str(remote_user))

            if ((self.max_usr < user and self.max_usr >= 0) or (
                            self.max_usr_local < local_user and self.max_usr_local >= 0) or (
                            self.max_usr_remote < remote_user and self.max_usr_remote >= 0)):
                self.logger.log("User: Not Ready for sleep! More users active than allowed!", 2)
                return 1

            self.logger.log("User: Ready for sleep!")
            return 0
        except:
            return -1

    @staticmethod
    def run():
        instance = usercheck()
        instance.logger.log("Usercheck: check started")
        return instance.check()

    @staticmethod
    def configure():
        configurable = []
        configurable.append(
            ["usercheck", "max_usr", '0', "amount of users logged in. nevertheless it's going to sleep | -1 = disable"])
        configurable.append(["usercheck", "max_usr_local", '-1',
                             "amount of users logged in local. nevertheless it's going to sleep | -1 = disable"])
        configurable.append(["usercheck", "max_usr_remote", '-1',
                             "amount of users logged in remotely. nevertheless it's going to sleep | -1 = disable"])
        configurable.append(["usercheck", "idle_timeout", '1800',
                             "time in sec. user which idle above this time are not counted | -1 = no timeout all user are counted"])
        return configurable

    def sleep(self):
        pass

    def wake(self):
        pass

# for testing purpose
if __name__ == '__main__':
    os.chdir('../')
    print(usercheck.run())
    print(usercheck.configure())
    print(usercheck.__doc__)
