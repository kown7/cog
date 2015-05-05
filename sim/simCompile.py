#!/usr/bin/python3

from cog import *
from conf import *

from subprocess import call, check_output
import sys
import pdb
import os
import re

from datetime import datetime
import time
import pprint


def simCompile():
        os.chdir(BASEDIR+'sim'+os.sep)

        try:  sys.argv.index('-f')
        except: forceCompile = False
        else: forceCompile = True

        #f = cog.cog( basedir=BASEDIR, top=TB_FILE, debug=1 )
        f = cog( basedir=BASEDIR, top=TB_FILE )
        f.comp = modelsimCompiler(MODELSIM)
        f.comp.compileOptions = COMPILE_OPTIONS

        f.runAll(forceCompile)
        return f

simCompile()
