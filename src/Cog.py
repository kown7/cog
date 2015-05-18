'''cog.py
Copyright (c) Kristoffer Nordstroem, All rights reserved.

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 3.0 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library.

------------------------------------------------------

Usage:
   In general the following:
    - setup config
    - load cache
    - load current compile times
    - TreeWalker parse
    - order list
    - compile
    - update compile times
    - store cache
    See also the runAll() function.

Compiler implementation need to implement the cogCompiler Interface
class.

The debug level needs to be set with the constructor
'''

import logging
import json
import os
import copy
import pdb
import pprint

from .TreeWalker import TreeWalker


class Cog(object):
    def __init__(self, **kwargs):
        self.libs = []
        if kwargs.get('basedir'):
            self.libs.append({'basedir' : kwargs.get('basedir', os.path.expanduser('~')),
                              'lib' : kwargs.get('lib', 'work'),
                              ## Directories not to be parsed; relative path to basedir
                              'exclude' : kwargs.get('exclude', [])})
        # File path needs to absolute
        self.top_file = os.path.abspath(kwargs.get('top', ''))
        # Should not be None, as it may trigger weird behaviour
        self.ignore_libs = kwargs.get('ignoreLibs', [])
        self.debug = kwargs.get('debug', False)
        # col : compile order list
        self.col = []
        # Assign compiler object to have runAll fun.
        self.comp = None

        self._cache = None
        self._parsed_tree = {}
        self._cache_file = os.path.join(os.path.expanduser('~'), '.cog.py.stash')

        if self.debug:
            logging.basicConfig(level=logging.DEBUG)

        #assert self.ignore_libs != None , 'ignoreLibs may not be None'

    def addLib(self, bdir, lib, exclude=None):
        if not exclude:
            exclude = []
        self.libs.append({'basedir' : bdir, 'lib' : lib, 'exclude' : exclude})

    def parse(self):
        for lib in self.libs:
            tw = TreeWalker(lib['basedir'], lib['lib'], '', lib['exclude'], self._cache)
            self._parsed_tree.update(tw.parse())


    def genTreeAll(self):
        self.col = self._generateDependencyTree(self._parsed_tree)


    def genTreeFile(self, *args):
        if len(args) > 0:
            self.top_file = os.path.abspath(args[0])
        if os.path.isfile(self.top_file):
            self.col = self._generateDependencyFile()
        else:
            logging.error('File does not exist: ' + self.top_file)


    def loadCache(self):
        try:
            with open(self._cache_file, 'r') as fp:
                self._cache = json.load(fp)
        except IOError:
            self._cache = None
            logging.warning('Could not open cache file')


    def importCompileTimes(self, designs):
        if not self._parsed_tree:
            raise Exception
        for inode in designs:
            if self._parsed_tree[inode]:
                try:
                    self._parsed_tree[inode].update({'ctime' : designs[inode]['ctime']})
                except KeyError:
                    logging.warning('No ctime found for ' + designs[inode]['name'])


    def saveCache(self):
        with open(self._cache_file, 'w') as f:
            f.write(json.dumps(self._cache))

    def printCsv(self):
        for obj in self.col:
            print(obj[0] + ',' + obj[1])

    def compileAll(self, forceCompile=False):
        self.loadCache()
        self.parse()
        if not forceCompile:
            self.importCompileTimes(self.comp.getLibsContent(self.libs))
        self.genTreeAll()
        self.comp.compileAllFiles(self.col)
        self.saveCache()


    def compile_file(self, force_compile=False):
        self.loadCache()
        self.parse()
        if not force_compile:
            self.importCompileTimes(self.comp.getLibsContent(self.libs))
        self.genTreeFile()
        self.comp.compileAllFiles(self.col)
        self.saveCache()        



    def _generateDependencyTree(self, parsedTreeInp):
        '''TODO: In order to prevent dependecies to be broken, we'd need to
        walk through the entire tree from both directions.

        '''
        ABORT_LIMIT = 10000
        iterCount = 0
        parsedTree = copy.copy(parsedTreeInp)
        col = [] # compile order list
        colIgnore = [] # dependencies not to be compiled
        colFp = [] # compile order list with filenames instead

        while len(parsedTree) > 0:
            for key in parsedTree:
                if self._isInCol(parsedTree[key]['deps'], colIgnore, parsedTree):
                    if parsedTree[key]['mtime'] < parsedTree[key]['ctime']:
                        colIgnore.append([parsedTree[key]['lib'], parsedTree[key]['objName']])
                    else:
                        col.append([parsedTree[key]['lib'], parsedTree[key]['objName']])
                        colFp.append([parsedTree[key]['lib'], parsedTree[key]['path'], parsedTree[key]['type']])
                    del parsedTree[key]
                    break
                elif self._isInCol(parsedTree[key]['deps'], col, parsedTree):
                    col.append([parsedTree[key]['lib'], parsedTree[key]['objName']])
                    colFp.append([parsedTree[key]['lib'], parsedTree[key]['path'], parsedTree[key]['type']])
                    del parsedTree[key]
                    break
                elif self._isInCol(parsedTree[key]['deps'], col+colIgnore, parsedTree):
                    col.append([parsedTree[key]['lib'], parsedTree[key]['objName']])
                    colFp.append([parsedTree[key]['lib'], parsedTree[key]['path'], parsedTree[key]['type']])
                    del parsedTree[key]
                    break
                    
            if iterCount == ABORT_LIMIT:
                pdb.set_trace()
                raise Exception
            else:
                iterCount += 1

        return colFp



    def _isInCol(self, deps, col, parsedTree):
        for dep in deps:
            try:
                self.ignore_libs.index(dep[0])
                continue # next element
            except ValueError:
                pass

            try:
                # Assume if library is not given, that it's a VHDL file
                # with default library 'work'
                if dep[0] == None:
                    col.index(['work', dep[1]])
                else:
                    col.index(dep)
            except ValueError:
                if dep[0] == None and self._isInTree(dep[1], parsedTree) == False:
                    pass
                else:
                    return False
        return True


    def _isInTree(self, entity, parsedTree):
        for key in parsedTree:
            if parsedTree[key]['objName'].lower() == entity:
                if parsedTree[key]['lib'].lower() != 'work':
                    logging.warning('Object ' + entity + ' found in library ' + parsedTree[key]['lib'])
                return True
        return False



    def _generateDependencyFile(self):
        absFilename = os.path.abspath(self.top_file)
        parsedTreeSubset = {}

        reqFiles = self._sampleReqFiles(absFilename)

        for i in reqFiles:
            parsedTreeSubset[i] = self._parsed_tree[i]

        return self._generateDependencyTree(parsedTreeSubset)


    def _sampleReqFiles(self, filename):
        absFilename = os.path.abspath(filename)
        curStat = os.stat(absFilename)
        curInodeStr = str(curStat.st_ino)
        reqFiles = [curInodeStr]

        for dep in self._parsed_tree[curInodeStr]['deps']:
            if len(dep) > 0:
                ret = self._callSampleReqFilesByObjName(dep)
                for i in ret:
                    try:
                        reqFiles.index(i)
                    except ValueError:
                        reqFiles.append(i)

        return reqFiles



    def _callSampleReqFilesByObjName(self, dep):
        for key in self._parsed_tree:
            if not self._parsed_tree[key]['objName']:
                continue # No name in file.
            if ((self._parsed_tree[key]['lib'].lower() == dep[0] or dep[0] == None) and
                    self._parsed_tree[key]['objName'].lower() == dep[1]):
                return self._sampleReqFiles(self._parsed_tree[key]['path'])
        logging.warning('Not found ' + str(dep))
        return []
