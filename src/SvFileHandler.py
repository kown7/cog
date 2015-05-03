import re

from .FileHandler import *

class SvFileHandler(FileHandler):
    def parse(self):
        cntParentheses = 0

        SvIdentifier = '[a-zA-Z][a-zA-Z0-9_]*'

        LineNum = 0
        with open(self.filePath, 'r') as f:
            for LineIn in f:
                LineNum += 1
                # Remove comments
                Line = LineIn.split('//',1)[0]
    
                # Search for entities instanciated 
                # Currently no modules et c. are extracted from SV
                m = re.search('('+SvIdentifier+')\s+i_('+SvIdentifier+')\s*\(', Line)
                if m != None:
                    logging.debug(self.library + ':DEP: ' + m.group(1))
                    self.dependsOnObject.append([self.library, m.group(1).lower()])
                
                if self.objectName == None:
                    m = re.search('module\s+('+SvIdentifier+')\s*;', Line.lower())
                    if m != None:
                        self.objectName = m.group(1)
                        logging.debug('Module:'+ str(LineNum) +': ' + m.group(1))
                        self.objectType = CogFileType.SvModule
                else:
                    cntParentheses += Line.count('(') - Line.count(')')
    
    
            if self.objectName == None:
                logging.warning('No object found in ' + str(self.filePath))
        
