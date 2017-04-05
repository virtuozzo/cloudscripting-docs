#! /bin/python
# -*- coding: utf-8 -*-

import os, sys, re

extension = ".md"
inputDir = "."

patternStr = ur'''@@@\s*(```\s*json.*?```)\s*(```\s*yaml.*?```)\s*@@!'''
repStr = ur'''@@@\n\2\n\1\n@@!'''

def replaceStringInFile(filePath):
    "replaces all string by a regex substitution"
    tempName = filePath+'~~~'
    inputFile = open(filePath)
    outputFile = open(tempName,'w')
    fContent = unicode(inputFile.read(), "utf-8")

    outText = re.sub(patternStr, repStr, fContent, 0, re.U|re.M|re.DOTALL)

    outputFile.write((outText.encode("utf-8")))

    outputFile.close()
    inputFile.close()

    os.rename(tempName, filePath)
    print "processed {}".format(filePath)

def fileFilter(dummyArg, thisDir, dirChildrenList):
    for thisChild in dirChildrenList:
        if extension == os.path.splitext(thisChild)[1] and os.path.isfile(thisDir+'/'+thisChild):
            replaceStringInFile(thisDir+'/'+thisChild)

os.path.walk(inputDir, fileFilter, None)