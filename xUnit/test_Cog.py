import unittest
import os
import pprint

from src import Cog

class CogUnittest(unittest.TestCase):

    def setUp(self):
        self.debug_info = False
        #self.debug_info = True
        self.PATH = os.path.join(os.path.dirname(__file__), 'vhdl')

        self.TB_FILE = os.path.join(self.PATH, 'A.vhd')
        self.coginst_one = Cog.Cog(top=self.TB_FILE, debug=self.debug_info)
        self.coginst_one.addLib(self.PATH, 'work')


    ###def test_dummy(self):
    ###    for x in range(1000):
    ###        self.assertEqual(x, x)

    def test_list_starting_with_A(self):
        expResp = ['Cents.vhd', 'B.vhd', 'A.vhd']
        
        #self.coginst_one.loadCache()
        self.coginst_one.parse()
        self.coginst_one.genTreeFile()

        actResp = []
        for i in self.coginst_one.col:
            actResp.append(i[1].split(os.sep)[-1])
            
        self.assertEqual(expResp, actResp)

if __name__ == '__main__':
    unittest.main()
