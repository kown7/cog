#!/usr/bin/python3

from cog import *

from subprocess import call, check_output
import sys
import pdb
import os
import re

from datetime import datetime
import time
import pprint
import configparser

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

config = configparser.ConfigParser()
config.read('conf.ini')
TB_ENTITY = config.get('General', 'TB_ENTITY')
COMPILE_OPTIONS = [x.strip() for x in config.get('General', 'COMPILE_OPTIONS').split(',')]
SIM_OPTIONS = [x.strip() for x in config.get('General', 'SIM_OPTIONS').split(',')]
MODELSIM = config.get('Files', 'MODELSIM')
BASEDIR = [x.strip() for x in config.get('Files', 'BASEDIR').split(',')]
TB_FILE = config.get('Files', 'TB_FILE')

simCompile()
