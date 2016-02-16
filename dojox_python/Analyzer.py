#!/usr/bin/python
# -*- coding: UTF-8 -*-

from __future__ import print_function

import os
import re
import sys

import yaml
import json

sys.path.insert(0, os.getcwd())

sys.stderr = sys.stdout


class Configuration:
    def __init__(self, filename):
        self.filename = filename
        with open(filename, 'r') as stream:
            self.environments = yaml.load(stream)

        for env, servers in self.environments.items():
            for server, components in servers.items():
                for (key,url) in components.items():
                    protocol = Configuration.protocol(url)
                    if protocol not in ['jar', 'file']:
                        raise InvalidConfiguration(protocol + ' not supported')

    def protocol(url):
        return url.split(':')[0]

    def server(url):
        return url.split(':')[1]

    def location(url):
        return url.split(':')[2]



class EnvCrawler:
    def __init__(self, connectorManager=None):
        self.connMgr = connectorManager

    def __crawl(self, environments):
        self.envDescr = {env: self.__crawlEnv(servers) for env, servers in environments.items()}

    def __crawlEnv(self, servers):
        return { server: self.__crawlServer( components ) for server, components in servers.items() }

    def __crawlServer(self, components):
        return { component: self.connMgr.connect(url) for (component, url) in components.items() }

    def envStatus(self):
        return json.dumps(self.envDescr)

class InvalidConfiguration(Exception):
    def __init__(self, errorMsg):
        pass


class Manifest:
    def __init__(self, contentString):
        self.content = {}
        if contentString != '':
            lines = contentString.split("\n")
            self.content = dict([Manifest.__splitKeyValue(line) for line in lines])

    def __splitKeyValue(keyvalue):
        vals = keyvalue.split(": ")
        return vals[0], vals[1].strip('\n\r')


class Connector:
    def __init__(self, protocol):
        self.protocol = protocol

    def connect(self, url):
        self.check(url)
        self.__executeRemote(self.command())

    def __executeRemote(self, cmd):
        pass

    def check(self, url):
        if (len(url.split(':')) != 3):
            raise InvalidConfiguration("The url '"+url+"' is not valid\n"+
                                       "The url should in the format : 'protocol:server:location'")

    def command(self):
        pass

class FileConnector(Connector):
    def __init__(self):
        super(FileConnector, self).__init__('file')

    def command(self, url):
        return "cat '" + Configuration.location(url) + "'"

class ZipConnector(Connector):
    def __init__(self):
        super(ZipConnector, self).__init__('zip')

    def command(self, url):
        return "unzip -p '"+Configuration.location(url)+"' META-INF/MANIFEST.MF"

class JarConnector(Connector):
    def __init__(self):
        super(JarConnector, self).__init__('jar')

    def connect(self, url):
        pass


class ConnectorManager:
    def __init__(self):
        self.connectors = {}

    def register(self, connector):
        self.connectors[connector.protocol] = connector
        return self

    def connect(self, url):
        protocol = Configuration.protocol(url)
        manifestContent = self.connectors[protocol].connect(url)
        return Manifest(manifestContent).content

        # if __name__ == '__main__':
        # try:
        #   ng = Configuration("aaa")
        #   ng.run()
        # except Exception as e:
        #     sys.stderr.write("Error into reducer : " + traceback.format_exc() + "\n")
        #     exit(-1)
