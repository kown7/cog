import os
import logging

from .CogFileType import CogFileType


class FileHandler(object):
    def __init__(self, path, filename, lib):
        self.path = path
        self.filename = filename
        self.lib = lib
        self.filePath = os.path.join(path, filename)

        self.objectName = None
        self.objectType = CogFileType.Undefined
        self.library = 'work'
        self.st_mtime = 0
        self.compileTime = 0
        self.dependsOnObject = []
        # Set to false if compile time and modification time has not
        # changed since last run.
        self.modified = True

        self._setChangeTime()
        self._setCompileTime()

    def _setChangeTime(self):
        stats = os.stat(self.filePath)
        self.st_mtime = stats.st_mtime

    def _setCompileTime(self):
        pass

    def getInfo(self):
        # ctime : compile time
        return {'path' : self.filePath, 'objName' : self.objectName,
                'lib' : self.library, 'deps' : self.dependsOnObject,
                'modified' : self.modified, 'mtime' : self.st_mtime,
                'ctime' : self.compileTime, 'type' : self.objectType}
