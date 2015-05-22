import re
import logging

from .FileHandler import FileHandler
from .CogFileType import CogFileType

class SvFileHandler(FileHandler):
    def parse(self):
        cnt_parentheses = 0

        sv_identifier = '[a-zA-Z][a-zA-Z0-9_]*'

        line_num = 0
        with open(self.file_path, 'r') as filep:
            for line_in in filep:
                line_num += 1
                # Remove comments
                line = line_in.split('//', 1)[0]

                # Search for entities instanciated
                # Currently no modules et c. are extracted from SV
                mtx = re.search(r'('+sv_identifier+r')\s+i_('+sv_identifier+r')\s*\(', line)
                if mtx != None:
                    logging.debug(self.library + ':DEP: ' + mtx.group(1))
                    self.depends_on_object.append([self.library, mtx.group(1).lower()])

                if self.object_name == None:
                    # The top-level module does not implement
                    # interfaces and the like, hence the ';'. Should
                    # be parameterized.
                    mtx = re.search(r'module\s+('+sv_identifier+r')\s*;', line.lower())
                    if mtx != None:
                        self.object_name = mtx.group(1)
                        logging.debug('Module:'+ str(line_num) +': ' + mtx.group(1))
                        self.object_type = CogFileType.SvModule
                else:
                    cnt_parentheses += line.count('(') - line.count(')')


            if self.object_name == None:
                logging.warning('No object found in ' + str(self.file_path))
