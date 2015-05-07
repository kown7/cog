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
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        try:  sys.argv.index('-f')
        except: forceCompile = False
        else: forceCompile = True

        #f = cog( basedir=BASEDIR, top=TB_FILE, debug=1 )
        f = cog( basedir=BASEDIR, top=TB_FILE )
        f.comp = modelsimCompiler(MODELSIM)
        f.comp.compileOptions = COMPILE_OPTIONS

        f.runAll(forceCompile)
        return f

simCompile()
