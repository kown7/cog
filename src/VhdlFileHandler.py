''' cog.py
Copyright (c) Kristoffer Nordström, All rights reserved.

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
'''

import re

from FileHandler import *

class VhdlFileHandler(FileHandler):
    def parse(self):
        cntParentheses = 0
        endFound = False
        # Simplified VHDL identifier; may not end with _ and no consecutive _
        # are allowed. But we're not a compiler...
        VhdlIdentifier = '[a-zA-Z][a-zA-Z0-9_]*'
        IgnoredLibraries = ['ieee', 'std'] 

        LineNum = 0
        f = open(self.filePath, 'r')
        for LineIn in f:
            LineNum += 1
            # Remove comments
            Line = LineIn.split('--',1)[0]

            # Search for libraries and packages used
            m = re.search('[uU][sS][eE]\s+('+VhdlIdentifier+')\.('+VhdlIdentifier+')\.', Line)
            if m != None:
                try:
                    IgnoredLibraries.index(m.group(1).lower())
                except:
                    logging.debug(m.group(1) + ': ' + m.group(2))
                    self.dependsOnObject.append([m.group(1).lower(), m.group(2).lower()])
            
            if self.objectName == None:
                m = re.search('(entity|package)\s+([a-z0-9_]+)\s+(?=is)', Line.lower())
                if m != None:
                    self.objectName = m.group(2)
                    logging.debug('Entity:'+ str(LineNum) +': ' + m.group(2))
                    if m.group(1) == "entity":
                        self.objectType = FileType.VhdlEntity
                    elif m.group(1) == 'package':
                        self.objectType = FileType.VhdlPackage
            else:
                cntParentheses += Line.count('(') - Line.count(')')

            if cntParentheses == 0 and self.objectName != None and endFound == False:
                m = re.search('end(\s*;|\s+(package\s+)*'+self.objectName.lower()+'\s*;)', Line.lower())
                if m != None:
                    logging.debug('End Object ' + self.objectName + ":" + str(LineNum))
                    endFound = True

            if endFound:
                m = re.search('component\s+(' + VhdlIdentifier + ')', Line.lower())
                if m != None:
                    logging.debug('Component:'+str(LineNum)+':' + m.group(1))
                    self.dependsOnObject.append([None, m.group(1)])
                
                m = re.search('entity\s+(('+ VhdlIdentifier + ')\.){0,1}(' + VhdlIdentifier +
                              ')\s+(?!is)', Line.lower())
                if m != None:
                    self.dependsOnObject.append([m.group(2), m.group(3)])
                

        if self.objectName == None:
            logging.warning('No object found in ' + str(self.filePath))
        elif endFound == False:
            logging.warning('Object ' + str(self.objectName) + ' has no ending: ' + str(self.filePath)
                            + ' ' + str(cntParentheses))

        f.close()
        
