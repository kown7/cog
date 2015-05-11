'''
Cog Environment
'''
import sys

from .CogConfiguration import CogConfiguration
from .Cog import Cog
from .modelsimCompiler import modelsimCompiler


class CogEnv(object):
    '''
    Setting up the Cog environment
      parse command-line and conf.ini file.
    '''
    def __init__(self):
        try:
            sys.argv.index('-f')
        except ValueError:
            self.force_compile = False
        else:
            self.force_compile = True

        try:
            sys.argv.index('--debug')
        except ValueError:
            debug_info = False
        else:
            debug_info = True

        self.cfg = CogConfiguration()

        self.coginst = Cog(top=self.cfg.TB_FILE, debug=debug_info)
        for i in self.cfg.BASEDIR:
            self.coginst.addLib(i, 'work')

        # Compiler factory
        if self.cfg.MODELSIM:
            self.coginst.comp = modelsimCompiler(self.cfg.MODELSIM)

        self.coginst.comp.compileOptions = self.cfg.COMPILE_OPTIONS

    def compile_all(self):
        self.coginst.compileAll(self.force_compile)

    def run_simulation_gui(self):
        self.coginst.comp.runSimulationGui(self.cfg.TB_ENTITY, self.cfg.SIM_OPTIONS)

    def run_simulation(self):
        self.coginst.comp.runSimulation(self.cfg.TB_ENTITY, self.cfg.SIM_OPTIONS)
