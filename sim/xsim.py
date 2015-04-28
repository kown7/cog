#!/usr/bin/python3

from subprocess import call

from conf import *
from simCompile import simCompile

simCompile()
call([VSIM,'-gui', '-do', 'wave.do', TB_ENTITY])
