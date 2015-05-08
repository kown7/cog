import configparser
import os
import sys
import pdb

import re
from datetime import datetime
import time
import pprint

from cog import *


class CogConfiguration(object):
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('conf.ini')

        self.TB_ENTITY = config.get('General', 'TB_ENTITY')
        self.COMPILE_OPTIONS = [x.strip() for x in config.get('General', 'COMPILE_OPTIONS').split(',')]
        self.SIM_OPTIONS = [x.strip() for x in config.get('General', 'SIM_OPTIONS').split(',')]
        self.MODELSIM = config.get('Files', 'MODELSIM')
        self.BASEDIR = [x.strip() for x in config.get('Files', 'BASEDIR').split(',')]
        self.TB_FILE = config.get('Files', 'TB_FILE')


def simCompile():
        try:  sys.argv.index('-f')
        except: forceCompile = False
        else: forceCompile = True
        
        cfg = CogConfiguration()
        pdb.set_trace()

        #f = cog( basedir=BASEDIR[0], top=TB_FILE, debug=1 )
        #f = cog( basedir=BASEDIR[0], top=TB_FILE )
        f = cog( top = cfg.TB_FILE )
        for i in cfg.BASEDIR:
                f.addLib(i, 'work')
        f.comp = modelsimCompiler(cfg.MODELSIM)
        f.comp.compileOptions = cfg.COMPILE_OPTIONS

        f.runAll(forceCompile)
        return [f, cfg]
