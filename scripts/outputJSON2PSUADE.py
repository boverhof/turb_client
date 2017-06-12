#!/usr/bin/env python
"""
JSON2Psuade

See Copyright for copyright notice!
"""
import sys, time, os
#from run_turbine import *
import json
from ConfigParser import ConfigParser
from turbine.commands.turbine_psuade_script import *
from turbine.commands.turbine_psuade_session_script import *
from turbine.commands import _open_config


if(sys.argv.__len__() < 5):
    print "Need an input json file, and input PSUADE file, an output PSAUDE file, and a config file."
    exit(1)


CP = _open_config(sys.argv[4])

certifyConfig(CP)

jsonFile = open(sys.argv[1], "r+")
inputJson = json.load(jsonFile);
jsonFile.close()

writeJson2Psuade(CP, inputJson, sys.argv[2], sys.argv[3]); 
                 #psuadeInFile, psuadeOutFile)


