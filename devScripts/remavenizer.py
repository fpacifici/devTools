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
Remavenizer script

This script provides some functionality to restructure a maven based project.

-modularize: takes a maven project or module, and converts it to a pom project putting
the content into an imported project.

-addmodule: creates a submodules for a pom project

-movesources: moves java sources and resources from one module to another one.

-mergemodules: picks two maven modules and merge them into one.

Created on Aug 2, 2012

@author: fpacifici
'''
import os
import shutil
from pomManagement.Pom import Pom

'''
Converts a java pom to a module pom. All the content of the java pom is moved into the module 
pom.
'''
def modularize(pomPath, newModuleName):
    #create new directory
    os.mkdir(pomPath+'/'+newModuleName)
    #copy everything but the pom
    for f in os.listdir(pomPath) :
        if f != 'pom.xml' and f != newModuleName:
            shutil.copytree(pomPath + '/' + f, pomPath + '/' + newModuleName + '/' + f)
    #create the new pom
    #merge plugins and dependencies
    pm = Pom()
    pmOrig = Pom(pomPath+'/pom.xml')
    head = pmOrig.getHead()
    pm.provideHead(head['groupId'] + '.' + head['artifactId'],newModuleName, head['version'], head['name'], head['packaging'], head['url'])
    pm.addPlugins(pmOrig.getPlugins())
    pm.addDependencies(pmOrig.getDependencies())
    pm.writeOut(pomPath + '/' + newModuleName + '/pom.xml')
    #change header of supoerpom and add modules
    pmOrig.provideHead(head['groupId'], head['artifactId'], head['version'], head['name'], 'pom', head['url'])
    newModule = pmOrig.buildModule(newModuleName)
    pmOrig.addModules([newModule])
    pmOrig.writeOut()
    pass

if __name__ == '__main__':
    pass