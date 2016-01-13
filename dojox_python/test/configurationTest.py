# -*- coding: UTF-8 -*-
__author__ = 'ks'

import unittest
import sys
import os
import logging
from  os.path import dirname
from datetime import date

from configuration import Configuration

sys.path.insert(0, os.path.join(dirname(__file__), "../src"))
sys.path.insert(0, "../src")


logging.basicConfig(level=logging.DEBUG)


class TestConfiguration(unittest.TestCase):
    # def setUp(self):

    def test_loadConfiguration(self):
        configuration = Configuration('config.yml')
        self.assertEquals( 'config.yml', configuration.filename )
        self.assertIsNotNone(configuration.environments)

    def test_invalidConfiguration(self):
        try:
            configuration = Configuration('confighyg.yml')
            self.assertEquals( 'config.yml', configuration.filename )
            self.fail()
        except FileNotFoundError as e:
            self.assertTrue("No such file" in e.__str__())



if __name__ == '__main__':
    unittest.main()
