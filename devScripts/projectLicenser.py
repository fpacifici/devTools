#!/usr/bin/env python
#
# Copyright 2012 Filippo Pacifici
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
'''
Project Licenser script.

It adds a given license template in front of every java file inside a 
project given the template file and the base directory of the project

It is able if requested to erase current template in front of package statement

Created on May 26, 2012

@author: fpacifici
'''
import os
import re
import sys
from os.path import join

def readLicense(fileName):
    f = open(fileName, 'r')
    ret = [line for line in f.readlines()]
    return ret

def listFiles(baseDir, rfilter):
    ret = []
    for root, dirs, files in os.walk(baseDir) :
        ret = ret + [root + '/' + f for f in files if re.match(rfilter,f)]
    return ret

def licenseFile(filename, license):
    fp = open(filename,'r')
    content = getContent(fp)
    fp.close()
    fp = open(filename,'w')
    fp.writelines(license)
    fp.write('\n')
    fp.writelines(content)
    fp.close()
    
def getContent(pfile):
    ret = []
    found = False
    for line in pfile.readlines() :
        if found or line.startswith("package "):
            found = True
        if found:
            ret.append(line)
    return ret

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Licenser script")
        print("It adds a license header to an entire java project")
        print("Usage: projectLicenser <license file> <project base dir>")
    else :
        lFile = sys.argv[1]
        baseDir = sys.argv[2]
        flicense = readLicense(lFile)
        for f in listFiles(baseDir, "^.*\.java$") :
            print (f)
            licenseFile(f, flicense)
