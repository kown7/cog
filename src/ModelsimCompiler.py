from .CogCompilerInterface import CogCompilerInterface
from .CogFileType import CogFileType
from .functions import str_fname_inode

from subprocess import call, check_output, CalledProcessError
import sys
#import pdb
import os
import re
import logging
from datetime import datetime
import time



def split_string_iter(foobar):
    return iter(foobar.splitlines())


class ModelsimCompiler(CogCompilerInterface):
    def __init__(self, path=None):
        self._modelsim_dir = None
        if path:
            self.modelsim_dir = path


    @property
    def modelsim_dir(self):
        return self._modelsim_dir
    @modelsim_dir.setter
    def modelsim_dir(self, val):
        self._modelsim_dir = val
        self.vlog = os.path.join(self._modelsim_dir, 'vlog.exe')
        self.vcom = os.path.join(self._modelsim_dir, 'vcom.exe')
        self.vlib = os.path.join(self._modelsim_dir, 'vlib.exe')
        self.vsim = os.path.join(self._modelsim_dir, 'vsim.exe')
        self.vdir = os.path.join(self._modelsim_dir, 'vdir.exe')


    def get_libs_content(self, libs):
        entities = {}
        if not self._modelsim_dir:
            raise Exception('Modelsim directory not specified.')
        for lib in libs:
            entities.update(self._get_lib_parsed(lib['lib']))
        return entities


    def _get_lib_parsed(self, cur_lib):
        lenv = self._modelsim_compensate_offset()
        if not os.path.isdir(cur_lib):
            try:
                call([self.vlib, cur_lib])
            except:
                raise SystemExit

        try:
            lib_cont = check_output([self.vdir, '-l', '-lib', cur_lib], env=lenv)
        except:
            print(self.vdir)
            raise Exception

        all_ents = {}
        cur_ent = {}
        for line_byte in split_string_iter(lib_cont):
            line = line_byte.decode("utf-8")
            match = re.search(r'\A([A-Z]+)\s+([A-z0-9_]+)', line)
            if match != None:
                # New entity found
                if len(cur_ent) > 0:
                    all_ents.update({inode : cur_ent})

                cur_ent = {'name' : match.group(2)}
            match = re.search(r'\s+Compile time: (.+)', line)
            if match != None:
                c_time = datetime.strptime(match.group(1), '%a %b %d %X %Y')
                cur_ent.update({'ctime' : time.mktime(c_time.timetuple())})
            match = re.search(r'\s+Source modified time: (.+)', line)
            if match != None:
                cur_ent.update({'mtime' : match.group(1)})
            match = re.search(r'\s+Source file: (.+)', line)
            if match != None:
                cur_ent.update({'path' : match.group(1)})
                inode = str_fname_inode(match.group(1))

        if len(cur_ent) > 0:
            all_ents.update({inode : cur_ent})
        return all_ents


    def _modelsim_compensate_offset(self):
        lenv = os.environ.copy()
        if sys.platform.startswith('cygwin'):
            # ff. ugly TZ hack, as it seems wrong on cygwin systems
            try:
                uoff = check_output(['date', "+'%z'"])
            except CalledProcessError:
                uoff = '+0000'

            try:
                utc_offset = uoff.decode('utf-8')
            except AttributeError:
                utc_offset = uoff

            lenv['TZ'] = 'UTC'+str(-int(utc_offset[1:4]))
        return lenv


    def compile_all_files(self, compile_order_list):
        lenv = self._modelsim_compensate_offset()

        for filep in compile_order_list:
            if filep[2] == CogFileType.VhdlEntity or filep[2] == CogFileType.VhdlPackage:
                compiler = self.vcom
            elif filep[2] == CogFileType.SvModule:
                compiler = self.vlog
            else:
                logging.warning('No compiler found for object: ' + filep[1])
                continue

            if sys.platform == 'cygwin':
                dec_fname = check_output(['cygpath.exe', '-w', filep[1]]).decode('utf-8').strip()
            else:
                dec_fname = filep[1]
            parms = [compiler]+self.compile_options+['-work', filep[0], dec_fname]
            i = call(parms, env=lenv)
            if i != 0:
                try:
                    input(Bcolors.WARNING+'Enter to terminate'+Bcolors.ENDC)
                except (SyntaxError, NameError):
                    raise SystemExit
                else:
                    raise SystemExit


    def run_simulation(self, dut_name, sim_options=None):
        if not sim_options:
            sim_options = []
        sim_options += ['-batch', '-onfinish', 'exit']
        try:
            sim_options.index('-do')
        except ValueError:
            sim_options += ['-do', 'run.do']
        return self._run_sim(dut_name, sim_options)


    def run_simulation_gui(self, dut_name, sim_options=None):
        if not sim_options:
            sim_options = []
        sim_options += ['-gui', '-onfinish', 'stop', '-do', 'wave.do']
        return self._run_sim(dut_name, sim_options)


    def _run_sim(self, dut_name, sim_options):
        if sim_options:
            self.simulation_options += sim_options
        try:
            output = check_output([self.vsim]+self.simulation_options+[dut_name])
        except CalledProcessError as err:
            output = err.output
            logging.warning('VSIM call failed with return code: ' + str(err.returncode))
            return err.returncode # Non-zero

        errors = 0
        warnings = 0
        notes = 0
        print_next = False
        out_split = output.split('\n')
        for line in out_split:
            if print_next:
                print(line)
                print_next = False
            if re.search(r'\*\* Failure:', line):
                print(line)
                return -42
            if re.search(r'\*\* Error:', line):
                print(line)
                print_next = True
                errors += 1
            if re.search(r'\*\* Warning:', line):
                print(line)
                print_next = True
                warnings += 1
            if re.search(r'\*\* Note:', line):
                print(line)
                notes += 1

        return errors + warnings




class Bcolors:
    #pylint: disable=invalid-name,unused-variable
    HEADER = ''
    OKBLUE = ''
    OKGREEN = ''
    WARNING = ''
    FAIL = ''
    ENDC = ''
    BOLD = ''
    UNDERLINE = ''

    def __init__(self):
        if not sys.platform.startswith('win'):
            self.HEADER = '\033[95m'
            self.OKBLUE = '\033[94m'
            self.OKGREEN = '\033[92m'
            self.WARNING = '\033[93m'
            self.FAIL = '\033[91m'
            self.ENDC = '\033[0m'
            self.BOLD = '\033[1m'
            self.UNDERLINE = '\033[4m'
