import re

from FileHandler import *

class VhdlFileHandler(FileHandler):
    def parse(self):
        cntParentheses = 0
        endFound = False

        f = open(self.filePath, 'r')
        for Line in f:
            
            if self.objectName == None:
                m = re.search('(entity|package)\s+([a-z0-9_]+)\s+is', Line.lower())
                if m != None:
                    self.objectName = m.group(2)
                    logging.debug('Entity: ' + m.group(2))
                    if m.group(1) == "entity":
                        self.objectType = FileType.VhdlEntity
                    elif m.group(1) == 'package':
                        self.objectType = FileType.VhdlPackage
            else:
                cntParentheses += Line.count('(') - Line.count(')')

            if cntParentheses == 0 and self.objectName != None:
                m = re.search('end(\s*;|\s+(package\s+)*'+self.objectName.lower()+'\s*;)', Line.lower())
                if m != None:
                    logging.debug('End found for object ' + self.objectName + ": " + Line)
                    endFound = True
                    break;

        if self.objectName == None:
            logging.warning('No object found in ' + str(self.filePath))
        elif endFound == False:
            logging.warning('Object ' + str(self.objectName) + ' has no ending: ' + str(self.filePath)
                            + ' ' + str(cntParentheses))
        
