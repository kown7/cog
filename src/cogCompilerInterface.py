class cogCompilerInterface(object):
    def getLibsContent(self, libs):
        # Useful but not necessry
        # Return { inode : { 'ctime' : some_time }}
        return {}

    def compileAllFiles(self, compile_order_list):
        raise NotImplementedError

    # The following functions are obviously not required, but the
    # simulation and compiler tools usually go hand-in-hand.  Should
    # return 0 if simulation successful, the number of errors/warnings
    # et c. otherwise.
    def runSimulation(self, dut_name, sim_options):
        raise NotImplementedError

    def runSimulationGui(self, dut_name, sim_options):
        raise NotImplementedError
