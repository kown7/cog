#!/usr/bin/python3

import os
from subprocess import call

from conf import *
from simCompile import simCompile

simCompile()
call([VSIM,'-gui', '-do', 'wave.do']+SIM_OPTIONS+[TB_ENTITY])
