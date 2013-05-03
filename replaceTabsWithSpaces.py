#!/usr/bin/python

import sys
import re

if len(sys.argv) == 2:
    fileName = sys.argv[1]

    fileRead = open(fileName, 'r').read()

    fileModify = re.sub("\t", "    ", fileRead)

    fileWrite = open(fileName, 'w')

    fileWrite.write(fileModify)

    fileWrite.close()
else:
    print "Give me one file to modify"
