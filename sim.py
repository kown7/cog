#!/usr/bin/python3
from cog import CogEnv

ce = CogEnv()
ce.compileAll()
rV = ce.runSimulation()

if rV: # Exit zero is good
    #pdb.set_trace()
    input('Not successful, enter to terminate')
    raise SystemExit
