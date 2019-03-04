#!/usr/bin/env python
"""
JSON2Psuade

See LICENSE.md for copyright notice!
"""
import sys
import time
import os
#from run_turbine import *
import json
from configparser import ConfigParser
from turbine.commands.turbine_csv_script import *
from turbine.commands.turbine_csv_session_script import *
from turbine.commands import _open_config


if(sys.argv.__len__() < 5):
    print("Need an input json file, and input PSUADE file, an output PSAUDE file, and a config file.")
    exit(1)


CP = _open_config(sys.argv[4])


jsonFile = open(sys.argv[1], "r+")
inputJson = json.load(jsonFile)
jsonFile.close()

writeJson2CSV(CP, inputJson, sys.argv[2], sys.argv[3])
# psuadeInFile, psuadeOutFile)
