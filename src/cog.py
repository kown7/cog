#!/usr/bin/python

import logging
from TreeWalker import *

print "I'll have my own compile-order generator, with blackjack and hookers."

basedir='/home/kristoffer/eedge/sourcecode'
xclude=['/tb']
#logging.basicConfig(level=logging.DEBUG)

f = TreeWalker(basedir, 'work', '.', None)
f.parse()

g = TreeWalker(basedir, 'work', '.', xclude)

