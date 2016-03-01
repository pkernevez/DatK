# -*- coding: UTF-8 -*-
__author__ = 'ks'

import logging
import unittest
import sys, os
from  os.path import dirname
from unittest.mock import MagicMock

sys.path.insert(0, os.path.join(dirname(__file__), ".."))
sys.path.insert(1, ".")
from analyzer import *

# sys.path.insert(0, os.path.join(dirname(__file__), "../src"))
# sys.path.insert(0, "../src")

logging.basicConfig(level=logging.DEBUG)


class TestAnalyzer(unittest.TestCase):
    # def setUp(self):

    def test_loadConfiguration(self):
        configuration = Configuration('config.yml')
        self.assertEquals('config.yml', configuration.filename)
        self.assertIsNotNone(configuration.environments)

    def test_loadIntegration(self):
        configuration = Configuration('config.yml')
        self.assertIsNotNone(configuration.environments['integration'])
        self.assertEquals("file:/data/tomcat/webapps/myapp/META-INF/MANIFEST",
                          configuration.environments['integration']['server1']['app1'])

    def test_getProtocol(self):
        self.assertEqual('file', Configuration.protocol('file:server1:/data/tomcat/webapps/myapp/META-INF/MANIFEST'))

    def test_getServer(self):
        self.assertEqual('server1', Configuration.server('file:server1:/data/tomcat/webapps/myapp/META-INF/MANIFEST'))

    def test_getLocation(self):
        self.assertEqual('/data/tomcat/webapps/myapp/META-INF/MANIFEST', Configuration.location('file:server1:/data/tomcat/webapps/myapp/META-INF/MANIFEST'))

    def test_bad_protocol(self):
        try:
            configuration = Configuration('bad_config.yml')
            self.fail()
        except InvalidConfiguration as e:
            self.assertTrue("not supported" in e.__str__())

    def test_invalidConfiguration(self):
        try:
            configuration = Configuration('confighyg.yml')
            self.assertEquals('config.yml', configuration.filename)
            self.fail()
        except FileNotFoundError as e:
            self.assertTrue("No such file" in e.__str__())

    def test_parseEmptyManifest(self):
        manifest = Manifest("")
        self.assertEqual({}, manifest.content)

    def test_parseManifestWithEmptyLines(self):
        manifest = Manifest("\r\n\r\n")
        self.assertEqual({}, manifest.content)

    def test_parseManifestWithOneCorrectLine(self):
        manifest = Manifest("Job-Name: origin/master")
        self.assertIsNotNone(manifest.content)
        self.assertEqual('origin/master', manifest.content['Job-Name'])

    def test_parseManifestWithTwoCorrectLines(self):
        manifest = Manifest("Job-Name: origin/master\nBuildDate: 2016-01-08 17:26")
        self.assertIsNotNone(manifest.content)
        self.assertEqual(2, manifest.content.__len__())
        self.assertEqual('origin/master', manifest.content['Job-Name'])
        self.assertEqual('2016-01-08 17:26', manifest.content['BuildDate'])

    def __registerMock(self, mgr, protocol, data):
        conn = MockConnector(protocol, data)
        mgr.register(conn)
        return self

    def test_registering_of_connector(self):
        mgr = ConnectorManager()
        self.__registerMock(mgr, 'jar', 'Job-Name: origin/master')
        self.assertEqual(1, len(mgr.connectors))

    def test_managerConnectToAppropriateConnector(self):
        mgr = ConnectorManager()
        jarConnector = MockConnector('jar', '')
        jarConnector.connect = MagicMock(return_value="")
        mgr.register(jarConnector)
        self.__registerMock(mgr, 'file', 'Job-Name: origin/master')
        mgr.connect("jar:server1:/data/appli2/programme.jar#META-INF/MANIFEST")
        jarConnector.connect.assert_called_with("jar:server1:/data/appli2/programme.jar#META-INF/MANIFEST")

    def test_managerConnectorReturnsValidManifest(self):
        mgr = ConnectorManager()
        self.__registerMock(mgr,'jar', 'BuildDate: 2016-01-08 17:26\nMain-Class: com.dojo.Main')
        manifest = mgr.connect("jar:/data/appli2/programme.jar#META-INF/MANIFEST")
        self.assertIsNotNone(manifest)
        self.assertEqual(2, len(manifest))
        self.assertEqual({"BuildDate": "2016-01-08 17:26", "Main-Class": "com.dojo.Main"}, manifest)

    def test_envCrawler(self):
        configuration = Configuration('config.yml')
        mgr = ConnectorManager()
        self.__registerMock(mgr, 'jar', 'BuildDate: 2016-01-08 17:26\nMain-Class: com.dojo.Main')
        self.__registerMock(mgr, 'file', 'BuildDate: 2016-01-14 17:26\nMain-Class: com.dojo.Nain')
        crawler = EnvCrawler( mgr)
        crawler._EnvCrawler__crawl(configuration.environments)
        envDesc = crawler.envDescr
        self.assertIsNotNone(envDesc)
        self.assertEqual(2, len(envDesc))
        self.assertIsNotNone(envDesc['integration'])
        self.assertEqual(2, len(envDesc['integration']))
        self.assertEqual(2, len(envDesc['integration']['server1']))
        self.assertEqual({'BuildDate': '2016-01-14 17:26', 'Main-Class': 'com.dojo.Nain'},
                         envDesc['integration']['server1']['app2'])

    def test_envStatusIsConvertedToJson(self):
        envDesc = EnvCrawler()
        envDesc.envDescr = {
            'integration': {
                'server1': {
                    'app1': {
                        'BuildDate': '2016-01-14 17:26'
        }}}}
        self.assertEqual('{"integration": {"server1": {"app1": {"BuildDate": "2016-01-14 17:26"}}}}', envDesc.envStatus())

    def test_envStatusIsWriteToFile(self):
        envCrawler = EnvCrawler()
        envCrawler.envDescr = {
            'integration': {
                'server1': {
                    'app1': {
                        'BuildDate': '2016-01-14 17:26'
        }}}}
        output = 'result.json'
        envCrawler._EnvCrawler__save(output)
        with open(output, 'r') as outputfile:
            self.assertEqual('{"integration": {"server1": {"app1": {"BuildDate": "2016-01-14 17:26"}}}}', outputfile.readline())
        os.remove(output)

    def test_FileConnector(self):
        conn = FileConnector()
        self.assertEqual("cat '/tmp/happystore/META-INF/MANIFEST.MF'",
                         conn.command('/tmp/happystore/META-INF/MANIFEST.MF'))

    def test_ZipConnector(self):
        conn = ZipConnector()
        self.assertEqual("unzip -p '/tmp/webapps/happystore.war' META-INF/MANIFEST.MF",
                         conn.command('/tmp/webapps/happystore.war'))

    # //TODO Ajouter jarConnector
    # // Gerer manifest multiline

    def test_errorMsgWhenInvalidUrl(self):
        conn = Connector('invalid')
        try:
            conn.connect("toto")
            self.fail("Should not passed !")
        except InvalidConfiguration as e:
            self.assertEqual("The url 'toto' is not valid\nThe url should in the format : 'protocol:server:location'", e.__str__())

class MockConnector(Connector):
    def __init__(self, protocol, data):
        super(MockConnector, self).__init__(protocol)
        self.data = data

    def connect(self, url):
        return self.data


if __name__ == '__main__':
    unittest.main()
