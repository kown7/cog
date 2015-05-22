class CogCompilerInterface(object):
    compile_options = []
    simulation_options = []


    def get_libs_content(self, libs):
        # Useful but not necessry
        # Return { inode : { 'ctime' : some_time }}
        return {}


    def compile_all_files(self, compile_order_list):
        raise NotImplementedError


    # The following functions are obviously not required, but the
    # simulation and compiler tools usually go hand-in-hand.  Should
    # return 0 if simulation successful, the number of errors/warnings
    # et c. otherwise.
    def run_simulation(self, dut_name, sim_options):
        raise NotImplementedError


    def run_simulation_gui(self, dut_name, sim_options):
        raise NotImplementedError
