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
        os.chdir(os.path.join(BASEDIR[0], 'sim'))

        try:  sys.argv.index('-f')
        except: forceCompile = False
        else: forceCompile = True

        #f = cog( basedir=BASEDIR[0], top=TB_FILE, debug=1 )
        #f = cog( basedir=BASEDIR[0], top=TB_FILE )
        f = cog( top = TB_FILE )
        for i in BASEDIR:
                f.addLib(i, 'work')
        f.comp = modelsimCompiler(MODELSIM)
        f.comp.compileOptions = COMPILE_OPTIONS

        f.runAll(forceCompile)
        return f
 
simCompile()
