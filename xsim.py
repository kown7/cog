#!/usr/bin/python3

from subprocess import call

from cog import *
from simCompile import *

f = simCompile()
f.comp.runSimulationGui(TB_ENTITY, SIM_OPTIONS)
#comp = modelsimCompiler(MODELSIM)
#call([comp.VSIM,'-gui', '-do', 'wave.do']+SIM_OPTIONS+[TB_ENTITY])
