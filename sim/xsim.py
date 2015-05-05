#!/usr/bin/python3

import os
from subprocess import call

from conf import *
from cog import *
from simCompile import simCompile

f = simCompile()
f.comp.runSimulationGui(TB_ENTITY, SIM_OPTIONS)
#comp = modelsimCompiler(MODELSIM)
#call([comp.VSIM,'-gui', '-do', 'wave.do']+SIM_OPTIONS+[TB_ENTITY])
