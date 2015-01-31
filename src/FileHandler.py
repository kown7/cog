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

        # This is now very VHDL nomeclatura
        self.objectName = None
        self.objectType = FileType.Undefined
        self.st_mtime = None
        self.compileTime = None

    def getInfo(self):
        return [ self.objectName, self.st_mtime, self.compileTime ]
