#!/usr/bin/python3
from cog import CogEnv

ce = CogEnv()
ce.compile_file()
rV = ce.run_simulation()

if rV: # Exit zero is good
    #pdb.set_trace()
    input('Not successful, enter to terminate')
    raise SystemExit
