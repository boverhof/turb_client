#!/usr/bin/env python
"""
psuade2JSON

See LICENSE.md for copyright notice!
"""

import sys,os
import json
import optparse
import sys
from configparser import ConfigParser

from turbine.commands.turbine_psuade_script import *
from turbine.commands.turbine_psuade_session_script import *
from turbine.commands import _open_config

if(sys.argv.__len__() < 4):
    print("Need an input file, an output file, and a config file.")
    exit(1)



CP = _open_config(sys.argv[3])

certifyConfig(CP)

samples = getInputsFromPSUADE_IO(CP, sys.argv[1])
inputsJson = writeInputsToGatewayFormat(CP, samples)

outfile = open(sys.argv[2], "w+")

outJsonString = json.dump(inputsJson, outfile, indent=2)

outfile.close()



