#from os import listdir 
import os
import logging

from VhdlFileHandler import *
from FileHandler import *

class TreeWalker(object):
    def __init__(self, basedir, lib, path, exclude, cached):
        self.basedir = basedir
        self.lib = lib
        self.path = path
        self.exclude = exclude
        self.curPath = basedir + path
        self.ls = os.listdir(self.curPath)
        self.curEntries = []
        self.thisDir = None
        self.cached = None
                
        self._setThisDir()
        self._findCachedEntry(cached)
        logging.debug(self.ls)

        
    def _setThisDir(self):
        fh = FileHandler(self.curPath, '', None)
        self.thisDir = fh.getInfo()

        
    def _findCachedEntry(self, cached):
        try: 
            i = len(cached)
            logging.debug('Length of cached: '+str(i))
        except:
            logging.debug('No length possible')
            self.cached = None
            return

        for k in range(0, i):
            for j in range(0,len(cached[k])):
                try:
                    if ((''.join(cached[k][j]['path']))) == self.curPath + '/':
                        if cached[k][j]['mtime'] == self.thisDir['mtime']:
                            #import pdb; pdb.set_trace()
                            self.cached = cached[k][j+1]
                            logging.debug('Cache:'+self.cached) 
                        break
                except Exception as e:
                    logging.debug ("Try failed: "+ str(e))

                
    def _findFileInCache(self, filename):
        if self.cached != None:
            for i in range(0, len(self.cached)):
                try:
                    if self.cached[i]['path'] == filename:
                        return i
                except:
                    pass 
            return None
        else:
            return None
            

    def _returnValues(self):
        return [self.thisDir, self.curEntries]

            
    def _parseCurPath(self):
        for i in self.ls:
            curStat = os.stat(self.curPath + '/' + i)
            logging.debug(i + ": " + str(curStat.st_mtime))
            if os.path.isdir(self.curPath + '/' + i):
                f = TreeWalker(self.basedir, self.lib, self.path + '/' + i, self.exclude, self.cached)
                self.curEntries.append(f.parse())
            elif i.lower().endswith(('.vhd', '.vhdl')):
                cacheIdx = self._findFileInCache(self.curPath + '/' + i)
                if cacheIdx == None:
                    logging.debug('VHDL file parsing: ' + i)
                    f = VhdlFileHandler(self.curPath, i, self.lib)
                    f.parse()
                    self.curEntries.append(f.getInfo())
                else:
                    self.curEntries.append(self.cached[cacheIdx])
                

    def parse(self):
        try:
            self.exclude.index(self.path)
            return []
        except:
            pass
        
        self._parseCurPath()
        return self._returnValues()
