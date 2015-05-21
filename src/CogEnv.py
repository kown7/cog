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
            self._debug_info = False
        else:
            self._debug_info = True

        self.cfg = CogConfiguration()
        if self.cfg.TB_ENTITY:
            self.factory()
        

    def factory(self):
        self.coginst = Cog(top=self.cfg.TB_FILE, debug=self._debug_info)
        for i in self.cfg.BASEDIR:
            self.coginst.add_lib(i, 'work')

        # Compiler factory
        if self.cfg.MODELSIM:
            self.coginst.comp = modelsimCompiler(self.cfg.MODELSIM)

        self.coginst.comp.compileOptions = self.cfg.COMPILE_OPTIONS

    def compile_all(self):
        self.coginst.compileAll(self.force_compile)

    def compile_file(self):
        self.coginst.compile_file(self.force_compile)

    def run_simulation_gui(self):
        return self.coginst.comp.runSimulationGui(self.cfg.TB_ENTITY, self.cfg.SIM_OPTIONS)

    def run_simulation(self):
        return self.coginst.comp.runSimulation(self.cfg.TB_ENTITY, self.cfg.SIM_OPTIONS)
