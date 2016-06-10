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

    def test_freeDirWhenNothingAround(self):
        grid = Grid()
        self.assertEqual({UP, DOWN, LEFT, RIGHT}, grid.free(5,5))

    def test_freeDirWhenCloseFromEdge(self):
        grid = Grid()
        self.assertEqual({UP, DOWN, RIGHT}, grid.free(0,5))
        self.assertEqual({UP, DOWN, LEFT}, grid.free(29,5))
        self.assertEqual({ DOWN, RIGHT, LEFT}, grid.free(5,0))
        self.assertEqual({ UP, RIGHT, LEFT}, grid.free(5,19))
        self.assertEqual({ DOWN, RIGHT}, grid.free(0,0))

    def test_freeDirAfterMoves(self):
        grid = Grid()
        grid.move(2,2)
        self.assertEqual({UP,DOWN,LEFT},grid.free(1,2))
        self.assertEqual({UP,DOWN,RIGHT},grid.free(3,2))
        self.assertEqual({UP,RIGHT,LEFT},grid.free(2,1))
        self.assertEqual({DOWN,RIGHT,LEFT},grid.free(2,3))

    def test_countDirectionWeigth(self):
        grid = Grid()
        self.assertEqual(27, grid.countFreeCells(2,2,RIGHT))