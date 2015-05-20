import unittest
import os
import pprint
import time

from src import Cog
from src import TestbenchCompiler

''' The test-setup looks as follows:

   A
   | - C
   | - B
       | - C

A depends on B and C; B depends on C only.
'''
class CogUnittest(unittest.TestCase):
    def setUp(self):
        self.debug_info = False
        #self.debug_info = True
        self.PATH = os.path.join(os.path.dirname(__file__), 'vhdl')
        self.TB_FILE = os.path.join(self.PATH, 'A.vhd')

        self.coginst_one = Cog.Cog(top=self.TB_FILE, debug=self.debug_info)
        self.coginst_one.addLib(self.PATH, 'work')

        self.coginst_two = Cog.Cog(top=self.TB_FILE, debug=self.debug_info)
        self.coginst_two.addLib(self.PATH, 'work')


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


    def test_compile_all_and_run_again_with_no_change(self):
        expResp = ['Cents.vhd', 'B.vhd', 'A.vhd']
        self.coginst_two.comp = TestbenchCompiler.TestbenchCompiler()
        self.coginst_two.compile_file(force_compile=True)
        actResp = []
        for i in self.coginst_two.col:
            actResp.append(i[1].split(os.sep)[-1])
        self.assertEqual(expResp, actResp)

        self.coginst_two.compile_file()
        expResp = []
        actResp = []
        for i in self.coginst_two.col:
            actResp.append(i[1].split(os.sep)[-1])
        self.assertEqual(expResp, actResp)


    def test_compile_all_and_run_again_with_B_changed(self):
        time.sleep(1) # Timestamps may be only 1s resolution.
        expResp = ['Cents.vhd', 'B.vhd', 'A.vhd']
        self.coginst_two.comp = TestbenchCompiler.TestbenchCompiler()
        self.coginst_two.compile_file(force_compile=True)
        actResp = []
        for i in self.coginst_two.col:
            actResp.append(i[1].split(os.sep)[-1])
        self.assertEqual(expResp, actResp)

        # Modify B.vhd
        time.sleep(1) # Timestamps may be only 1s resolution.
        os.utime(self.coginst_two.col[1][1])

        self.coginst_two.compile_file()
        expResp = ['B.vhd', 'A.vhd']
        actResp = []
        for i in self.coginst_two.col:
            actResp.append(i[1].split(os.sep)[-1])
        self.assertEqual(expResp, actResp)



if __name__ == '__main__':
    unittest.main()
