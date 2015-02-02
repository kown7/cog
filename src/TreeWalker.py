#from os import listdir 
import os
import logging

from VhdlFileHandler import *
#from FileHandler import *

class TreeWalker(object):
    def __init__(self, basedir, lib, path, exclude, cached):
        self.basedir = basedir
        self.lib = lib
        self.path = path
        self.exclude = exclude
        self.curPath = basedir + path
        self.ls = os.listdir(self.curPath)
        self.curEntries = {}
        self.cached = cached
                
        logging.debug(self.ls)

                
    def _returnValues(self):
        return self.curEntries

            
    def _parseCurPath(self):
        for i in self.ls:
            curPath = self.curPath + '/' + i
            curStat = os.stat(curPath)
            curInodeStr = str(curStat.st_ino)
            logging.debug(i + ": " + str(curStat.st_mtime))
            if os.path.isdir(curPath):
                f = TreeWalker(self.basedir, self.lib, self.path + '/' + i, self.exclude, self.cached)
                self.curEntries.update(f.parse())
            elif i.lower().endswith(('.vhd', '.vhdl')):
                try:
                    if (self.cached[curInodeStr]['path'] == curPath and
                        self.cached[curInodeStr]['mtime'] == curStat.st_mtime):
                        # TODO : Account for compile time changes as well here
                        self.curEntries[curInodeStr] = self.cached[curInodeStr]
                        self.curEntries[curInodeStr]['modified'] = False
                    else:
                        print ('raise E')
                        raise Exception
                except:
                    logging.debug('VHDL file parsing: ' + i)
                    f = VhdlFileHandler(self.curPath, i, self.lib)
                    f.parse()
                    self.curEntries.update({str(curStat.st_ino) : f.getInfo()})
                

    def parse(self):
        try:
            self.exclude.index(self.path)
            return []
        except:
            pass
        
        self._parseCurPath()
        return self._returnValues()
