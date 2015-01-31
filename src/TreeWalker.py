#from os import listdir 
import os
import logging

from VhdlFileHandler import *

class TreeWalker(object):
    def __init__(self, basedir, lib, path, exclude):
        self.basedir = basedir
        self.lib = lib
        self.path = path
        self.exclude = exclude
        self.curPath = basedir + '/' + path
        
        self.ls = os.listdir(self.curPath)
        logging.debug(self.ls)

    def parse(self):
        try:
            exclude.index(path)
        except:
            self.parseCurPath()

    def parseCurPath(self):
        for i in self.ls:
            curStat = os.stat(self.curPath + '/' + i)
            logging.debug(i + ": " + str(curStat.st_mtime))
            if os.path.isdir(self.curPath + '/' + i):
                f = TreeWalker(self.basedir, self.lib, self.path + '/' + i, self.exclude)
                f.parse()
            elif i.lower().endswith(('.vhd', '.vhdl')):
                logging.debug('VHDL file found: ' + i)
                f = VhdlFileHandler(self.curPath, i, self.lib)
                f.parse()
                print f.getInfo()
