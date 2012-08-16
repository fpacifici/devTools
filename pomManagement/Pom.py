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

Created on Aug 2, 2012

@author: fpacifici
'''
from xml.dom import minidom


class Pom(object):
    '''
    This class represents a POM file, it allows to add / remove elements 
    both if the pom file is read from the beginning and if the pom is created from scratch.
    '''

    def __init__(self, fileName = None):
        '''
        Constructor.
        If fileName is not null it loads the pom from the fileName
        If fileName is Null it prepares the structure of an empty pom.
        '''
        if fileName != None:
            self.pomDoc = minidom.parse(fileName)
            self.fileName = fileName
        else:
            impl = minidom.getDOMImplementation()
            self.pomDoc = impl.createDocument('http://maven.apache.org/POM/4.0.0', 'project',None)
            fchild = self.pomDoc.firstChild
            fchild.setAttribute('xmlns','http://maven.apache.org/POM/4.0.0')
            fchild.setAttribute('xmlns:xsi','http://www.w3.org/2001/XMLSchema-instance')
            fchild.setAttribute('xsi:schemaLocation','http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd')
            

    def writeOut(self, fileName = None):
        '''
        Writes out the pom. 
        If fileName is specified, that's the output, otherwise the one 
        used to load the pom is used. If the pom was created from scratch
        the fileName must be specified.
        '''
        fn = None
        if fileName == None:
            if self.fileName == None:
                raise Exception('Cannot write out: no file name specified')
            else:
                fn = self.fileName
        else:
            fn = fileName
            
        outpString = self.pomDoc.toprettyxml(' ', '\n')
        f = open(fn,'w')
        f.write(outpString)
        f.close()
        
    def toxml(self):
        '''
        Returns the output string
        '''
        return self.pomDoc.toprettyxml()
        

    def provideHead(self, groupId, artifact, version, name , packaging, url):
        '''
        Sets the header of the pom.
        '''
        self.__checkAndSetTextNode('modelVersion', '4.0.0')
        self.__checkAndSetTextNode('groupId', groupId)
        self.__checkAndSetTextNode('artifactId', artifact)
        self.__checkAndSetTextNode('version', version)
        if name != None:
            self.__checkAndSetTextNode('name', name)
        self.__checkAndSetTextNode('packaging', packaging)
        if url != None:
            self.__checkAndSetTextNode('url', url)
            
    def getHead(self):
        '''
        Returns the existing head
        '''
        ret = {}
        ret['groupId'] = self.__returnElement('groupId')
        ret['artifactId'] = self.__returnElement('artifactId')
        ret['version'] = self.__returnElement('version')
        ret['name'] = self.__returnElement('name')
        ret['packaging'] = self.__returnElement('packaging')
        ret['url'] = self.__returnElement('url')
        return ret    
    
    def getDependencies(self):
        '''
        gets the dependencies as a list of dictionaries
        '''
        dependElement = self.pomDoc.getElementsByTagName('dependencies')
        if len(dependElement) > 0:
            return [i for i in dependElement[0].childNodes if i.nodeType != i.TEXT_NODE]
        else:
            return []
        
    def addDependencies(self, dependencies):
        '''
        adds dependencies as list of dictionaries
        '''
        listDeps = self.__getListToUpdate('dependencies')
        self.__mergeElements('dependency',listDeps, dependencies, 
                             [('artifactId',None),('groupId',None)])
    
    def getPlugins(self):
        '''
        returns the plugins as a list of dictionaries
        '''
        buildElements = self.pomDoc.getElementsByTagName('build')
        if len(buildElements) > 0:
            pluginsElement = self.pomDoc.getElementsByTagName('plugins')
            if len(pluginsElement) > 0:
                return [i for i in pluginsElement[0].childNodes if i.nodeType != i.TEXT_NODE]
        return []
        
    def addPlugins(self, plugins):
        '''
        adds plugins as list of dictionaries
        '''
        buildElem = self.pomDoc.getElementsByTagName('build')
        if len(buildElem) == 0:
            buildElem = self.pomDoc.createElement('build')
        self.pomDoc.firstChild.appendChild(buildElem) 
        listDeps = self.__getListToUpdate('plugins',buildElem)
        self.__mergeElements('plugin',listDeps, plugins, 
                             [('artifactId',None)])
        
    def getModules(self):
        '''
        returns the modules as a list of dictionaries
        '''
        pluginsElement = self.pomDoc.getElementsByTagName('modules')
        if len(pluginsElement) > 0:
            return pluginsElement[0].childNodes
        else:
            return []
    
    def addModules(self, modules):
        '''
        adds modules as list of dictionaries
        '''
        listDeps = self.__getListToUpdate('modules')
        self.__mergeElements('module',listDeps, modules, [])
        
    def buildModule(self, moduleName):
        '''
        builds a module element
        '''
        modScaffolding = self.pomDoc.createElement('module')
        modScaffolding.appendChild(self.pomDoc.createTextNode(moduleName))
        return modScaffolding
    
    def __getListToUpdate(self, elemName, root = None):
        #get the list of elements to merge or create it if needed
        if root == None :
            root = self.pomDoc.firstChild
        currentDependencyElement = root.getElementsByTagName(elemName)
        
        listDeps = None
        if len(currentDependencyElement) > 0 :
            listDeps = currentDependencyElement[0].childNodes
        else:
            depElement = self.pomDoc.createElement(elemName)
            root.appendChild(depElement)   
            listDeps = depElement.childNodes 
        return listDeps
    
    def __returnElement(self, elementName):
        elToUseList = self.pomDoc.getElementsByTagName(elementName)
        elToUse = None
        elToUse = elToUseList[0]
        child = elToUse.firstChild
        return child.data
        
    
    def __checkAndSetTextNode(self, elementName, textValue):
        #get a reference to the node and create if not
        elToUseList = self.pomDoc.getElementsByTagName(elementName)
        elToUse = None
        if len(elToUseList) == 0 :
            #create and append
            elToUse = self.pomDoc.createElement(elementName)
            self.pomDoc.firstChild.appendChild(elToUse)
        else:
            elToUse = elToUseList[0]
        child = elToUse.firstChild
        
        #get reference to text content and create if not exists
        if child == None :
            #create, and add
            textEl = self.pomDoc.createTextNode(textValue)
            elToUse.appendChild(textEl)
        else:
            #retrieve and change content
            textEl = child
            textEl.replaceWholeText(textValue)
    
    def __mergeElements(self, goodTagName,destination, elementList, idXPaths ):
        '''
        merges a list of elements inot another one.
        a list of idXPaths are provided to ensure the element is not
        already present.
        Already present elements are skipped
        '''
        ret = destination
        extIndex = []
        for el in destination:
            if el.__class__.__name__ == 'Element' and el.tagName == goodTagName:
                eid = self.getId(el, idXPaths)
                extIndex.append(eid)
        #not performs the merge
        for el in elementList:
            eid = self.getId(el, idXPaths)
            if not eid in extIndex:
                ret.append(el)
        return ret
        
    def getId(self, element, idXPaths):
        '''
        Extracts the id elements from a DOM elements 
        as sepcified in idXPaths, where idXPaths is in reality a tree
        identifying the set of elements that constitute the id
        where the leaves are elements.
        '''
        return self.__doGetId(element, idXPaths, [])
    
    def __doGetId(self, element, currentLevel, currentSolution):
        '''
        Internal version to be called recursively
        '''
        currentSolution
        ret = []
        for name in  sorted(currentLevel) :
            children = element.getElementsByTagName(name[0])
            if len (children) == 0 :
                raise Exception ('Cannot create ID. Element %s not present' % str(currentLevel))
            else:    
                if name[1] == None:
                    thisChild = children[0]
                    ret.append(self.__getText(thisChild.childNodes))
                else:
                    ret+= self.__doGetId(children[0],name[1],currentSolution)
        return currentSolution + ret
    
    def __getText(self,nodeList):
        rc = []
        for node in nodeList:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data.lstrip())
        return ''.join(rc)    