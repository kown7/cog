import configparser
import pdb

from .CogConfiguration import CogConfiguration
from .cog import cog
from .modelsimCompiler import modelsimCompiler


class CogEnv(object):
    def __init__(self):
        try:  sys.argv.index('-f')
        except: self.forceCompile = False
        else: self.forceCompile = True
        
        try:  sys.argv.index('--debug')
        except: debugInfo = False
        else: debugInfo = True
        
        self.cfg = CogConfiguration()

        self.f = cog( top = self.cfg.TB_FILE, debug = debugInfo )
        for i in self.cfg.BASEDIR:
            self.f.addLib(i, 'work')

        # Compiler factory
        if self.cfg.MODELSIM:
            self.f.comp = modelsimCompiler(self.cfg.MODELSIM)
            
        self.f.comp.compileOptions = self.cfg.COMPILE_OPTIONS

    def compileAll(self):
        self.f.compileAll(self.forceCompile)

    def runSimulationGui(self):
        self.f.comp.runSimulationGui(self.cfg.TB_ENTITY, self.cfg.SIM_OPTIONS)

    def runSimulation(self):
        self.f.comp.runSimulation(self.cfg.TB_ENTITY, self.cfg.SIM_OPTIONS)
