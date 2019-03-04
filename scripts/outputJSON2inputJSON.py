#!/usr/bin/env python
"""
outputJSON2inputJSON.py

Takes a set of JSON result from the server and turns it back into an input set for resubmission.  (Handy for testing purposes)

See LICENSE.md for copyright notice!
"""

import sys,os
import json

if(sys.argv.__len__() != 3):
    print("USAGE: outputJSON2inputJSON.py outputJSONFile inputJSONFile")
    sys.exit(1)

infile = open(sys.argv[1], "r+")
outfile = open(sys.argv[2], "w+")

fullset = json.load(infile)

inputset = []

for thisrun in fullset:
    thisinput = {}
    thisinput["Simulation"] = thisrun["Simulation"]
    thisinput["Inputs"] = json.loads(thisrun["Input"][0])
    inputset.append(thisinput)

json.dump(inputset, outfile, indent=2)

infile.close()
outfile.close()
