#!/usr/bin/python3

'''
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

import logging
import json
import os
import pprint
import copy

from TreeWalker import *

print("I'll have my own compile-order-generator (cog), with blackjack and hookers.")

basedir='/home/kristoffer/eedge/sourcecode/'
xclude=['/tb']
# Should not be None, as it may trigger wierd behaviour
ignoreLibs=['fsa0a_c_generic_core', 'fsa0a_c_generic_core', 'fsa0a_c_t33_generic_io']
assert ignoreLibs != None , 'ignoreLibs may not be None'
#logging.basicConfig(level=logging.DEBUG)


def generateDependencyTree(parsedTreeInp):
    ABORT_LIMIT = 10000
    iterCount = 0
    parsedTree = copy.copy(parsedTreeInp)
    col = [] # compile order list
    colFp = [] # compile order list with filenames instead
    
    while len(parsedTree) > 0:
        for key in parsedTree:
            if isInCol(parsedTree[key]['deps'], col, parsedTree):
                col.append([parsedTree[key]['lib'], parsedTree[key]['objName']])
                colFp.append([parsedTree[key]['lib'], parsedTree[key]['path']])
                del parsedTree[key]
                break
        if iterCount == ABORT_LIMIT:
            #pprint.pprint(col)
            #pprint.pprint(parsedTree)
            raise Exception
        else:
            iterCount += 1
            
    return colFp



def isInCol(deps, col, parsedTree):
    for dep in deps:
        try:
            ignoreLibs.index(dep[0])
            continue # next element
        except:
            pass
            
        try:
            # Assume if library is not given, that it's a VHDL file
            # with default library 'work'
            if dep[0] == None:
                col.index(['work', dep[1]])
            else:
                col.index(dep)
        except:
            if dep[0] == None and isInTree(dep[1], parsedTree) == False:
                pass
            else:
                return False
    return True


def isInTree(entity, parsedTree):
    for key in parsedTree:
        if parsedTree[key]['objName'].lower() == entity:
            if parsedTree[key]['lib'].lower() != 'work':
                loggin.warning('Object ' + entity + ' found in library ' + parsedTree[key]['lib'])
            return True
    return False



def generateDependencyFile(parsedTree, filename):
    absFilename = os.path.abspath(filename)
    parsedTreeSubset = {}
    
    reqFiles = _sampleReqFiles(parsedTree, absFilename)
    print (reqFiles)
    
    for i in reqFiles:
        parsedTreeSubset[i] = parsedTree[i]

    return generateDependencyTree(parsedTreeSubset)
    

def _sampleReqFiles(parsedTree, filename):
    absFilename = os.path.abspath(filename)
    curStat = os.stat(absFilename)
    curInodeStr = str(curStat.st_ino)
    reqFiles = [curInodeStr]

    for dep in parsedTree[curInodeStr]['deps']:
        if len(dep) > 0:
            ret = _callSampleReqFilesByObjName(parsedTree, dep)
            for i in ret:
                try:
                    reqFiles.index(i)
                except:
                    reqFiles.append(i)

    return reqFiles
            


def _callSampleReqFilesByObjName(parsedTree, dep):
    for key in parsedTree:
        if ((parsedTree[key]['lib'].lower() == dep[0] or dep[0] == None)
            and parsedTree[key]['objName'].lower() == dep[1]):
            return _sampleReqFiles(parsedTree, parsedTree[key]['path'])
    logging.warning('Not found ' + str(dep))
    return []

    
f = TreeWalker(basedir, 'work', '', None, None)
fparsed = f.parse()
#pprint.pprint (generateDependencyTree(fparsed))
pprint.pprint (generateDependencyFile(fparsed, basedir+'/HardOut.vhd' ))

print ('-----------------------------------------------')
#g = TreeWalker(basedir, 'work', '', xclude, None)
#gparsed = g.parse()
#pprint.pprint (generateDependencyTree(gparsed))


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
    hparsed = h.parse()
    f.write(json.dumps(hparsed))

col = generateDependencyTree(hparsed)
pprint.pprint (col)
#pprint.pprint (hparsed)
print(len(hparsed))

