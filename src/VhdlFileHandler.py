''' cog.py
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
'''

import re
import logging

from .FileHandler import FileHandler
from .CogFileType import CogFileType

class VhdlFileHandler(FileHandler):
    def parse(self):
        cnt_parentheses = 0
        end_found = False
        # Simplified VHDL identifier; may not end with _ and no consecutive _
        # are allowed. But we're not a compiler...
        vhdl_identifier = '[a-zA-Z][a-zA-Z0-9_]*'
        ignored_libs = ['ieee', 'std']

        line_num = 0
        with open(self.file_path, 'r') as filep:
            for line_in in filep:
                line_num += 1
                # Remove comments
                line = line_in.split('--', 1)[0]

                # Search for libraries and packages used
                mtx = re.search(r'[uU][sS][eE]\s+('+vhdl_identifier+r')\.('+vhdl_identifier+r')\.', line)
                if mtx != None:
                    try:
                        ignored_libs.index(mtx.group(1).lower())
                    except ValueError:
                        logging.debug(mtx.group(1) + ': ' + mtx.group(2))
                        self.depends_on_object.append([mtx.group(1).lower(), mtx.group(2).lower()])

                if self.object_name == None:
                    mtx = re.search(r'(entity|package)\s+([a-z0-9_]+)\s+(?=is)', line.lower())
                    if mtx != None:
                        self.object_name = mtx.group(2)
                        logging.debug('Entity:'+ str(line_num) +': ' + mtx.group(2))
                        if mtx.group(1) == "entity":
                            self.object_type = CogFileType.VhdlEntity
                        elif mtx.group(1) == 'package':
                            self.object_type = CogFileType.VhdlPackage
                else:
                    cnt_parentheses += line.count('(') - line.count(')')

                if cnt_parentheses == 0 and self.object_name != None and end_found == False:
                    mtx = re.search(r'end(\s*;|\s+((entity|package)\s+)*'
                                    +self.object_name.lower()+r'\s*;)', line.lower())
                    if mtx != None:
                        logging.debug('End Object ' + self.object_name + ":" + str(line_num))
                        end_found = True

                if end_found:
                    mtx = re.search(r'component\s+(' + vhdl_identifier + ')', line.lower())
                    if mtx != None:
                        logging.debug('Component:'+str(line_num)+':' + mtx.group(1))
                        self.depends_on_object.append([None, mtx.group(1)])

                    mtx = re.search(r'entity\s+(('+ vhdl_identifier + r')\.){0,1}(' + vhdl_identifier +
                                    r')\s+(?!is)', line.lower())
                    if mtx != None:
                        self.depends_on_object.append([mtx.group(2), mtx.group(3)])


            if self.object_name == None:
                logging.warning('No object found in ' + str(self.file_path))
            elif end_found == False:
                logging.warning('Object ' + str(self.object_name) + ' has no ending: ' + str(self.file_path)
                                + ' ' + str(cnt_parentheses))
