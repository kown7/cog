#!/usr/bin/python3

'''
General behaviour:
 - setup config 
 - load cache
 - load current compile times
 - TreeWalker parse
 - order List
 - compile
 - update compile times
 - store cache
''' 

import logging
import json
import os
import pprint
import copy

from TreeWalker import *

class cog(object):
    def __init__(self, **kwargs):
        self.basedir = kwargs.get('basedir', os.path.expanduser('~'))
        self.lib = kwargs.get('lib', 'work')
        # Directories not to be parsed; relative to basedir
        self.exclude = kwargs.get('exclude', [])
        # File path needs to absolute
        self.topFile = os.path.abspath(kwargs.get('top', None))
        # Should not be None, as it may trigger weird behaviour
        self.ignoreLibs = kwargs.get('ignoreLibs', [])
        self.debug = kwargs.get('debug', False)
        self.col = []

        self._cache = None
        self._parsedTree = None
        self._cacheFile = os.path.expanduser('~') + '/.cog.py.stash'
        
        if self.debug:
            logging.basicConfig(level=logging.DEBUG)

        #assert self.ignoreLibs != None , 'ignoreLibs may not be None'
        
    
    def parse(self):
        tw = TreeWalker(self.basedir, self.lib, '', self.exclude, self._cache)
        self._parsedTree = tw.parse()

    def genTreeAll(self):
        self.col = self._generateDependencyTree(self._parsedTree)

    def genTreeFile(self, *args):
        if len(args) > 0:
            self.topFile = os.path.abspath(args[0])
        if os.path.isfile(self.topFile):
            self.col = self._generateDependencyFile()
        else:
            logging.error('File does not exist: ' + self.topFile)
            
            
    def loadCache(self):
        try:
            with open(self._cacheFile, 'r') as fp:
                self._cache = json.load(fp)
        except:
            self._cache = None
            loggin.warning('Could not open cache file')

            
    def saveCache(self):
        with open(self._cacheFile, 'w') as f:
            f.write(json.dumps(self._cache))
        

    def _generateDependencyTree(self, parsedTreeInp):
        ABORT_LIMIT = 10000
        iterCount = 0
        parsedTree = copy.copy(parsedTreeInp)
        col = [] # compile order list
        colFp = [] # compile order list with filenames instead

        while len(parsedTree) > 0:
            for key in parsedTree:
                if self._isInCol(parsedTree[key]['deps'], col, parsedTree):
                    col.append([parsedTree[key]['lib'], parsedTree[key]['objName']])
                    colFp.append([parsedTree[key]['lib'], parsedTree[key]['path']])
                    del parsedTree[key]
                    break
            if iterCount == ABORT_LIMIT:
                #pprint.pprint(col)
                #pprint.pprint(parsedTree)
                raise Exception
            else:
                iterCount += 1

        return colFp



    def _isInCol(self, deps, col, parsedTree):
        for dep in deps:
            try:
                self.ignoreLibs.index(dep[0])
                continue # next element
            except:
                pass

            try:
                # Assume if library is not given, that it's a VHDL file
                # with default library 'work'
                if dep[0] == None:
                    col.index(['work', dep[1]])
                else:
                    col.index(dep)
            except:
                if dep[0] == None and self._isInTree(dep[1], parsedTree) == False:
                    pass
                else:
                    return False
        return True


    def _isInTree(self, entity, parsedTree):
        for key in parsedTree:
            if parsedTree[key]['objName'].lower() == entity:
                if parsedTree[key]['lib'].lower() != 'work':
                    loggin.warning('Object ' + entity + ' found in library ' + parsedTree[key]['lib'])
                return True
        return False



    def _generateDependencyFile(self):
        absFilename = os.path.abspath(self.topFile)
        parsedTreeSubset = {}

        reqFiles = self._sampleReqFiles(absFilename)

        for i in reqFiles:
            parsedTreeSubset[i] = self._parsedTree[i]

        return self._generateDependencyTree(parsedTreeSubset)


    def _sampleReqFiles(self, filename):
        absFilename = os.path.abspath(filename)
        curStat = os.stat(absFilename)
        curInodeStr = str(curStat.st_ino)
        reqFiles = [curInodeStr]

        for dep in self._parsedTree[curInodeStr]['deps']:
            if len(dep) > 0:
                ret = self._callSampleReqFilesByObjName(dep)
                for i in ret:
                    try:
                        reqFiles.index(i)
                    except:
                        reqFiles.append(i)

        return reqFiles



    def _callSampleReqFilesByObjName(self, dep):
        for key in self._parsedTree:
            if ((self._parsedTree[key]['lib'].lower() == dep[0] or dep[0] == None)
                and self._parsedTree[key]['objName'].lower() == dep[1]):
                return self._sampleReqFiles(self._parsedTree[key]['path'])
        logging.warning('Not found ' + str(dep))
        return []

