# -*- coding: UTF-8 -*-
__author__ = 'ks'

import logging
import os
import unittest
from  os.path import dirname

from Main import *

sys.path.insert(0, os.path.join(dirname(__file__), ".."))
sys.path.insert(1, ".")

# sys.path.insert(0, os.path.join(dirname(__file__), "../src"))
# sys.path.insert(0, "../src")

logging.basicConfig(level=logging.DEBUG)




class TestAnalyzer(unittest.TestCase):



    def setUp(self):
        None


    def test_validGridSize(self):
        grid = Grid()
        self.assertEqual(30, len(grid.grid))
        self.assertEqual(20, len(grid.grid[0]))

    def test_gridInit(self):
        grid = Grid()
        self.assertEqual(0, grid.grid[3][4])
        self.assertEqual(0, grid.grid[24][14])
        self.assertEqual(0, grid.grid[29][7])

    def test_positionPassed(self):
        grid = Grid()
        grid.move(7,3)

        self.assertEqual(1,grid.grid[7][3])