#!/usr/bin/python3
import pdb
from conf import *

[f, cfg] = simCompile()
f.comp.runSimulationGui(cfg.TB_ENTITY, cfg.SIM_OPTIONS)


