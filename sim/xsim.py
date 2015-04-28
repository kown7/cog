#!/usr/bin/python3

from subprocess import call

from conf import *
from simCompile import simCompile

simCompile()
call([XSIM, TB_ENTITY])
