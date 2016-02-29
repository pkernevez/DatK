#!/usr/bin/python
# -*- coding: UTF-8 -*-

from __future__ import print_function

import os
import re
import sys
import traceback
from subprocess import check_output
import subprocess

import yaml
import json
import logging

sys.path.insert(0, os.getcwd())

sys.stderr = sys.stdout

logging.basicConfig(format='%(asctime)-15s %(levelname)s %(message)s', level='DEBUG')


class Configuration:
    def __init__(self, filename):
        self.filename = filename
        logging.debug("Loading %s", filename)
        with open(filename, 'r') as stream:
            self.environments = yaml.load(stream)

        for env, servers in self.environments.items():
            for server, components in servers.items():
                for (key,url) in components.items():
                    protocol = Configuration.protocol(url)
                    if protocol not in ['jar', 'file']:
                        raise InvalidConfiguration(protocol + ' not supported')
        logging.info("Configuration loaded. Found {0} environnement(s)".format(len(self.environments.items())))

    def protocol(url):
        return url.split(':')[0]

    def server(url):
        return url.split(':')[1]

    def location(url):
        return url.split(':')[2]



class EnvCrawler:
    def __init__(self, connectorManager=None):
        self.connMgr = connectorManager
        self.envDescr = {}

    def crawl(self, configuration, outputfile):
        self.__crawl(configuration.environments)
        self.__save(outputfile)

    def __save(self, file):
        try:
            os.remove(file)
        except OSError:
            pass
        with open(file, 'w') as out:
            out.write( self.envStatus() )


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
            self.content = dict([Manifest.__splitKeyValue(line) for line in lines if len(line)>3])

    def __splitKeyValue(keyvalue):
        vals = keyvalue.split(": ")
        return vals[0], vals[1].strip('\n\r')




class Connector:
    def __init__(self, protocol):
        self.protocol = protocol

    def connect(self, url):
        self.check(url)
        return self.__executeRemote(url)

    def __executeRemote(self, url):
        cmd = self.command(Configuration.location(url))
        server = Configuration.server(url)
        logging.debug('Execute : ssh %s %s', server, cmd)
        result = check_output(["ssh", server, cmd], stderr=subprocess.STDOUT)
        logging.debug('Result of execution is : %s', result)
        return result.decode("utf-8")

    def check(self, url):
        if (len(url.split(':')) != 3):
            raise InvalidConfiguration("The url '"+url+"' is not valid\n"+
                                       "The url should in the format : 'protocol:server:location'")

    def command(self, location):
        pass




class FileConnector(Connector):
    def __init__(self):
        super(FileConnector, self).__init__('file')

    def command(self, location):
        return "cat '" + location + "'"

class ZipConnector(Connector):
    def __init__(self):
        super(ZipConnector, self).__init__('zip')

    def command(self, location):
        return "unzip -p '"+location+"' META-INF/MANIFEST.MF"

class JarConnector(Connector):
    def __init__(self):
        super(JarConnector, self).__init__('jar')

    def connect(self, location):
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



if __name__ == '__main__':
    if len(sys.argv) != 3:
        logging.error("Invalid parameters !")
        logging.error("Usage : analyzer.py config.yaml result.json")
        exit(-2)
    try:
        conf = Configuration(sys.argv[1])
        mgr = ConnectorManager()
        mgr.register(FileConnector())
        mgr.register(JarConnector())
        mgr.register(ZipConnector())
        EnvCrawler(mgr).crawl(conf, sys.argv[2])
    except Exception as e:
        sys.stderr.write("Error when collecting informations : " + traceback.format_exc() + "\n")
        exit(-1)
