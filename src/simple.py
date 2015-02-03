#!/usr/bin/python3

'''This file is an example file on how to use the cog.py. It is
considered public domain. Everything in the cog is covered by the
license README.md


General behaviour:
 - setup config 
 - load cache
 - load current compile times
 - TreeWalker parse
 - order List
 - compile
 - update compile times
 - store cache

''' 

import pprint
import cog

print("I'll have my own compile-order-generator (cog), with blackjack and hookers.")

f = cog.cog( basedir = '/home/kristoffer/eedge', top='../../eedge/sourcecode/HardOut.vhd',
          ignoreLibs = ['fsa0a_c_generic_core', 'fsa0a_c_generic_core', 'fsa0a_c_t33_generic_io'])
f.loadCache()
f.parse()
f.genTreeFile()
pprint.pprint(f.col)
f.saveCache()
print ('------------------------------------------------')
f.printCsv()
