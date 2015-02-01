#from os import listdir 
import os
import logging

class FileType(object):
    Undefined = None
    VhdlEntity = 1
    VhdlPackage = 2

class FileHandler(object):
    def __init__(self, path, filename, lib):
        self.path = path
        self.filename = filename
        self.lib = lib
        self.filePath = path + '/' + filename

        self.objectName = None
        self.objectType = FileType.Undefined
        self.st_mtime = None
        self.compileTime = None
        self.dependsOnObject = []

        self._setChangeTime()
        self._setCompileTime()

    def _setChangeTime(self):
        stats = os.stat(self.filePath)
        self.st_mtime = stats.st_mtime
        
    def _setCompileTime(self):
        pass

    def getInfo(self):
        return { 'path' : self.filePath, 'objName' : self.objectName, 'deps' :  
                 self.dependsOnObject, 'mtime' : self.st_mtime, 'compTime' : self.compileTime }
