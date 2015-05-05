#!/usr/bin/python3

import pdb
import os
from subprocess import call

from conf import *
from cog import *

from simCompile import simCompile

f = simCompile()
rV = f.comp.runSimulation(TB_ENTITY, SIM_OPTIONS)

if rV: # Exit zero is good
    #pdb.set_trace()
    input('Not successful, enter to terminate')
    raise SystemExit
