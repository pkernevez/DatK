#!/usr/bin/python
# -*- coding: UTF-8 -*-

from __future__ import print_function

import os
import re
import sys

import yaml

sys.path.insert(0, os.getcwd())

sys.stderr = sys.stdout


class Configuration:
    def __init__(self, filename):
        self.filename = filename
        with open(filename, 'r') as stream:
            self.environments = yaml.load(stream)

        for env, servers in self.environments.items():
            for server, urls in servers.items():
                for url in urls:
                    protocol = Configuration.protocol(url)
                    if protocol not in ['jar', 'file']:
                        raise InvalidConfiguration(protocol + ' not supported')

    def protocol(url):
        return re.search('^(.*):', url).group(1)


class InvalidConfiguration(Exception):
    def __init__(self, errorMsg):
        pass


class Manifest:

    def __init__(self, contentString):
        self.content = {}
        if contentString != '':
            lines = contentString.split("\n")
            for line in lines:
                vals = line.split(": ")
                self.content[vals[0]] = vals[1].strip('\n\r')
                #TODO fro compèrehnsion


class Connector:
    def __init__(self, protocol):
        self.protocol = protocol

    def connect(self, url):
        return ""


class ConnectorManager:
    def __init__(self):
        self.connectors = {}

    def register(self, connector):
        self.connectors[connector.protocol] = connector
        return self

    def connect(self, url):
        protocol = Configuration.protocol(url)
        manifestContent = self.connectors[protocol].connect(url)

        return manifestContent

        # if __name__ == '__main__':
        # try:
        #   ng = Configuration("aaa")
        #   ng.run()
        # except Exception as e:
        #     sys.stderr.write("Error into reducer : " + traceback.format_exc() + "\n")
        #     exit(-1)
