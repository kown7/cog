#!/usr/bin/python3

import logging
import json
import os
import pprint

from TreeWalker import *


print("I'll have my own compile-order generator, with blackjack and hookers.")

basedir='/home/kristoffer/eedge/sourcecode/'
xclude=['/tb']
#logging.basicConfig(level=logging.DEBUG)

f = TreeWalker(basedir, 'work', '', None, None)
print (f.parse())

print ('-----------------------------------------------')
g = TreeWalker(basedir, 'work', '', xclude, None)
print (g.parse())



print ('===============================================')
home = os.path.expanduser('~')
try:
    with open(home + '/.cog.py.stash', 'r') as f:
        hcached = json.load(f)
except:
    hcached = None
h = TreeWalker('/home/kristoffer/I2C_Slave', 'work', '', None, hcached)
print ('-----------------------------------------------')
with open(home + '/.cog.py.stash', 'w') as f:
    hparsed = []
    hparsed.append(h.parse())
    #pprint.pprint (hparsed)
    f.write(json.dumps(hparsed))
