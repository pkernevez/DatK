# -*- coding: UTF-8 -*-
__author__ = 'ks'

import unittest
import sys
import os
import logging
from  os.path import dirname
from datetime import date

from configuration import *

sys.path.insert(0, os.path.join(dirname(__file__), "../src"))
sys.path.insert(0, "../src")


logging.basicConfig(level=logging.DEBUG)


class TestConfiguration(unittest.TestCase):
    # def setUp(self):

    def test_loadConfiguration(self):
        configuration = Configuration('config.yml')
        self.assertEquals( 'config.yml', configuration.filename )
        self.assertIsNotNone(configuration.environments)

    def test_loadIntegration(self):
        configuration = Configuration('config.yml')
        self.assertIsNotNone(configuration.environments['integration'])
        self.assertEquals("file:/data/tomcat/webapps/myapp/META-INF/MANIFEST", configuration.environments['integration']['server1'][0])


    def test_bad_protocol(self):
        try:
            configuration = Configuration('bad_config.yml')
            self.fail()
        except InvalidConfiguration as e:
            self.assertTrue("not supported" in e.__str__())

    def test_invalidConfiguration(self):
        try:
            configuration = Configuration('confighyg.yml')
            self.assertEquals( 'config.yml', configuration.filename )
            self.fail()
        except FileNotFoundError as e:
            self.assertTrue("No such file" in e.__str__())

    def test_parseManifest(self):
        manifest = Manifest("MANIFEST.MF")
        manifestContent = manifest.parse()
        self.assertIsNotNone(manifestContent)
        self.assertEqual('origin/master', manifestContent['Job-Name'])

    def test_file_connector(self):
        connector = Connector('file')
        connector.connect('file:/blah/blah')



    def test_registering_of_connector(self):
        mgr = ConnectorManager()
        mgr.register( MockConnector('jar', 'Job-Name: origin/master') )
        self.assertEqual(1, len( mgr.connectors))



class MockConnector (Connector):
    def __init__(self, protocol, data):
        super(MockConnector, self).__init__(protocol)
        self.data = data

    def connect(self, url):
        return self.data

if __name__ == '__main__':
    unittest.main()
