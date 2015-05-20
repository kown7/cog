import time
import logging

from .cogCompilerInterface import *
from .functions import str_fname_inode


class TestbenchCompiler(cogCompilerInterface):
    '''This compiler only generates compile-time timestamp the given time
    it's been called. Can be retrieved in the same instance at the
    moment only.
    '''
    def __init__(self):
        self._virtual_lib = None

    def getLibsContent(self, libs):
        if not self._virtual_lib:
            raise NotImplementedError

        entities = {}
        for lib in libs:
            entities.update(self._virtual_lib[lib['lib']])
        return entities


    def compileAllFiles(self, compile_order_list):
        virtual_lib = {}
        # Required to compile list generated by cog.
        for i in compile_order_list:
            inode = str_fname_inode(i[1])
            ctime = time.time()
            lib = i[0]

            logging.debug('Entity: ' + i[1] + ' in library ' + i[0])

            try:
                virtual_lib[lib].update({inode : {'ctime' : ctime}})
            except KeyError:
                virtual_lib.update({lib : {inode : {'ctime' : ctime}}})

        self._virtual_lib = virtual_lib

    # The following functions are obviously not required, but the
    # simulation and compiler tools usually go hand-in-hand.
    def runSimulation(self, dut_name, sim_options):
        raise NotImplementedError

    def runSimulationGui(self, dut_name, sim_options):
        raise NotImplementedError
