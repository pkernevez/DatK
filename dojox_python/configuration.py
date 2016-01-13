#!/usr/bin/python
# -*- coding: UTF-8 -*-

from __future__ import print_function

import os
import sys
import traceback
import yaml


sys.path.insert(0, os.getcwd())

sys.stderr = sys.stdout


class Configuration:

    def __init__(self, filename):
        self.filename = filename
        with open(filename, 'r') as stream:
            self.environments = yaml.load(stream)


#if __name__ == '__main__':
    #try:
     #   ng = Configuration("aaa")
     #   ng.run()
    # except Exception as e:
    #     sys.stderr.write("Error into reducer : " + traceback.format_exc() + "\n")
    #     exit(-1)