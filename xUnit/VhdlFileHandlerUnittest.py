import unittest
import os
from ..src import VhdlFileHandler
from ..src import CogFileType

class VhdlFileHandlerUnittest(unittest.TestCase):

    def setUp(self):
        self.TEST_FILE_NAME = 'test1.vhd'
        self.PATH = os.path.join(os.path.dirname(__file__), 'vhdl')
        
        self.vfh = VhdlFileHandler.VhdlFileHandler(self.PATH, self.TEST_FILE_NAME, 'work')

        
    ##def test_dummy(self):
    ##    for x in range(1000):
    ##        self.assertEqual(x, x)

    def test_test1(self):
        expResp = {'path' : os.path.join(self.PATH, self.TEST_FILE_NAME),
                   'objName' : 'test1',
                   'lib' : 'work',
                   'deps' : [],
                   'type' : CogFileType.CogFileType.VhdlEntity}
        #'modified' : self.modified, 'mtime' : self.st_mtime,
        #'ctime' : self.compileTime}
        self.vfh.parse()
        actResp = self.vfh.getInfo()

        self.assertEqual(actResp['path'], expResp['path'])
        self.assertEqual(actResp['objName'], expResp['objName'])
        self.assertEqual(actResp['lib'], expResp['lib'])
        self.assertEqual(actResp['deps'], expResp['deps'])
        self.assertEqual(actResp['type'], expResp['type'])
    
        
if __name__ == '__main__':
    unittest.main()



