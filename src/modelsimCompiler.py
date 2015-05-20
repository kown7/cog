from .cogCompilerInterface import *
from .CogFileType import *
from .functions import *

from subprocess import call, check_output, CalledProcessError
import sys
import pdb
import os
import re
import logging

from datetime import datetime
import time
import pprint


def splitStringIter(foobar): return iter(foobar.splitlines())


class modelsimCompiler(cogCompilerInterface):
    def __init__(self, path = None):
        if path:
            self.modelsimDir = path

    @property
    def modelsimDir(self):
        return self._modelsimDir
    @modelsimDir.setter
    def modelsimDir(self, val):
        self._modelsimDir = val
        self.VLOG = os.path.join(self._modelsimDir, 'vlog.exe')
        self.VCOM = os.path.join(self._modelsimDir, 'vcom.exe')
        self.VLIB = os.path.join(self._modelsimDir, 'vlib.exe')
        self.VSIM = os.path.join(self._modelsimDir, 'vsim.exe')
        self.VDIR = os.path.join(self._modelsimDir, 'vdir.exe')
    _modelsimDir = None

    compileOptions = []
    simulationOptions  = []


    def getLibsContent(self, libs):
        entities = {}
        if not self._modelsimDir:
            raise Exception('Modelsim directory not specified.')
        for lib in libs:
            entities.update(self._getLibParsed(lib['lib']))
        return entities


    def _getLibParsed(self, curLib):
        lenv=self._modelsimCompensateOffset()
        if not os.path.isdir(curLib):
            try: call([self.VLIB, curLib])
            except: raise SystemExit

        try:
            libContent = check_output([self.VDIR, '-l', '-lib', curLib], env=lenv)
        except:
            print(self.VDIR)
            raise(Exception)

        allEnt = {}
        curEnt = {}
        for lineByte in splitStringIter(libContent):
                line = lineByte.decode("utf-8")
                m = re.search('\A([A-Z]+)\s+([A-z0-9_]+)', line)
                if m != None:
                        # New entity found
                        if len(curEnt) > 0:
                                allEnt.update({inode : curEnt})

                        curEnt = {'name' : m.group(2)}
                m = re.search('\s+Compile time: (.+)', line)
                if m != None:
                        cTime = datetime.strptime(m.group(1), '%a %b %d %X %Y')
                        curEnt.update({'ctime' : time.mktime(cTime.timetuple()) })
                m = re.search('\s+Source modified time: (.+)', line)
                if m != None:
                        curEnt.update({'mtime' : m.group(1)})
                m = re.search('\s+Source file: (.+)', line)
                if m != None:
                        curEnt.update({'path' : m.group(1)})
                        inode = str_fname_inode(m.group(1))

        if len(curEnt) > 0:
                allEnt.update({inode : curEnt})
        return allEnt


    def _modelsimCompensateOffset(self):
        lenv = os.environ.copy()
        if sys.platform.startswith('cygwin'):
                # ff. ugly TZ hack, as it seems wrong on cygwin systems
                try:
                        uoff = check_output(['date', "+'%z'"])
                except:
                        uoff = '+0000'

                try:
                        UTCoffset = uoff.decode('utf-8')
                except:
                        UTCoffset = uoff

                lenv['TZ'] = 'UTC'+str(-int(UTCoffset[1:4]))
        return lenv


    def compileAllFiles(self, compile_order_list):
        lenv=self._modelsimCompensateOffset()

        for fp in compile_order_list:
                if fp[2] == CogFileType.VhdlEntity or fp[2] == CogFileType.VhdlPackage:
                    compiler = self.VCOM
                elif fp[2] == CogFileType.SvModule:
                    compiler = self.VLOG
                else:
                    logging.warning('No compiler found for object: ' + fp[1])
                    continue

                if sys.platform == 'cygwin':
                    decFname = check_output(['cygpath.exe', '-w', fp[1]]).decode('utf-8').strip()
                else:
                    decFname = fp[1]
                parms = [compiler]+self.compileOptions+['-work', fp[0], decFname]
                i = call(parms, env=lenv)
                if i != 0:
                        input(bcolors.WARNING+'Enter to terminate'+bcolors.ENDC)
                        raise SystemExit


    def runSimulation(self, dut_name, sim_options = []):
        sim_options+= ['-batch', '-onfinish', 'exit']
        try:
            sim_options.index('-do')
        except ValueError:
            sim_options += ['-do', 'run.do']
        return self._runSim(dut_name, sim_options)


    def runSimulationGui(self, dut_name, sim_options = []):
        sim_options += ['-gui', '-onfinish', 'stop', '-do', 'wave.do']
        return self._runSim(dut_name, sim_options)


    def _runSim(self, dut_name, sim_options):
        if sim_options:
            self.simulationOptions += sim_options;
        try:
            output = check_output([self.VSIM]+self.simulationOptions+[dut_name])
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
            if re.search('\*\* Failure:', line):
                print(line)
                return -42
            if re.search('\*\* Error:', line):
                print(line)
                print_next = True
                errors += 1
            if re.search('\*\* Warning:', line):
                print(line)
                print_next = True
                warnings += 1
            if re.search('\*\* Note:', line):
                print(line)
                notes += 1

        return errors + warnings




class bcolors:
        if not sys.platform.startswith('win'):
                HEADER = '\033[95m'
                OKBLUE = '\033[94m'
                OKGREEN = '\033[92m'
                WARNING = '\033[93m'
                FAIL = '\033[91m'
                ENDC = '\033[0m'
                BOLD = '\033[1m'
                UNDERLINE = '\033[4m'
        else:
                HEADER = ''
                OKBLUE = ''
                OKGREEN = ''
                WARNING = ''
                FAIL = ''
                ENDC = ''
                BOLD = ''
                UNDERLINE = ''
