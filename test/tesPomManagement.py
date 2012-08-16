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
Tests the usage of Pom class in pomManagement package.

Created on Aug 3, 2012

@author: fpacifici
'''
from pomManagement.Pom import Pom
from xml.dom import minidom

#build a brand new pom
expected = '<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"/>'
    

def testGetId():
    XPaths = [('dependencies',[('dependency',[('artifactId',None),('groupId',None)])])]
    
    newP2 = Pom()
    pomDoc = minidom.parse('pom.xml')
    id = newP2.getId(pomDoc.firstChild, XPaths)
    
    print id

def testAddDependencies():
    newP2 = Pom('pom.xml')
    impl = minidom.getDOMImplementation()
    pomDoc = impl.createDocument('http://maven.apache.org/POM/4.0.0', 'project',None)
    deps = []
    
    e1 = pomDoc.createElement('dependency')
    e12 = pomDoc.createElement('groupId')
    et12 = pomDoc.createTextNode('bu')
    e12.childNodes.append(et12)
    e1.childNodes.append(e12)
    e13 = pomDoc.createElement('artifactId')
    et13 = pomDoc.createTextNode('ba')
    e13.childNodes.append(et13)
    e1.childNodes.append(e13)
    deps.append(e1)
    
    newP2.addDependencies(deps)

    print newP2.toxml()

def testMerge():
    newP3 = Pom('pom.xml')
    newModule = newP3.buildModule('myModule')
    newP3.addModules([newModule])
    newP3.writeOut()

if __name__ == '__main__':
    
    newP = Pom()
    st = newP.toxml()
    assert (st.count(expected) == 1)
    
    #set the header
    newP.provideHead('org.twitterNotifier', 'twitterNotifier', '0.1-SNAPSHOT','','','')
    st = newP.toxml()
    
    assert(st.count('org.twitterNotifier') > 0)
    assert(st.count('0.1-SNAPSHOT') > 0)
    assert(st.count('4.0.0') > 0)
    
    #reset the header
    newP.provideHead('org.whateverelse', 'whateverelse', '1.0','','','')
    st = newP.toxml()
    #print(st)
    
    assert(st.count('org.whateverelse') > 0)
    assert(st.count('whateverelse') > 0)
    assert(st.count('1.0') > 0)
    
    testGetId()
    testAddDependencies()