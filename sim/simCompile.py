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
        print(os.getcwd())

        #f = cog.cog( basedir=BASEDIR, top=TB_FILE, debug=1 )
        f = cog( basedir=BASEDIR, top=TB_FILE )
        f.comp = modelsimCompiler(MODELSIM)
        f.comp.compileOptions = COMPILE_OPTIONS
        
        f.loadCache()
        f.parse()
        try:  sys.argv.index('-f')
        except:  f.importCompileTimes(f.comp.getLibsContent(f.libs))
        f.genTreeAll()
        f.comp.compileAllFiles(f.col)
        f.saveCache()
        #pdb.set_trace()
        return f

simCompile()
