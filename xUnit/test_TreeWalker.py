import unittest
import os
import pprint
from src import TreeWalker
from src import CogFileType

class TreeWalkerUnittest(unittest.TestCase):

    def setUp(self):
        self.NESTED_FILE_NAME = 'A.vhd'
        self.PATH = os.path.join(os.path.dirname(__file__), 'vhdl')

        self.nested_tree_walker = TreeWalker.TreeWalker(self.PATH, 'work', '.', [], None)


    ###def test_dummy(self):
    ###    for x in range(1000):
    ###        self.assertEqual(x, x)

    def test_find_all_entities_in_vhdl_subdir(self):
        expResp = ['test1', 'a', 'b', 'cents']
        outputList = []
        dir_content = self.nested_tree_walker.parse()
        for key, obj in dir_content.items():
            try:
                i = expResp.index(obj['objName'])
            except:
                continue
            else:
                del expResp[i]

        self.assertEqual(expResp, [])

if __name__ == '__main__':
    unittest.main()
