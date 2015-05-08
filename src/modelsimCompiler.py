from .cogCompilerInterface import *
from .CogFileType import *
from subprocess import call, check_output
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
    
        
    def getLibsContent(self, libs = ['work']):
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
                        curStat = os.stat(m.group(1))
                        inode = str(curStat.st_ino)

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


    def compileAllFiles(self, compileOrderList):
        lenv=self._modelsimCompensateOffset()

        for fp in compileOrderList:
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


    def runSimulation(self, dutName, simOpts = []):
        simOpts += ['-batch', '-do', 'run.do']
        return self._runSim(dutName, simOpts)
        
    def runSimulationGui(self, dutName, simOpts = []):
        simOpts += ['-gui', '-onfinish', 'stop', '-do', 'wave.do']
        return self._runSim(dutName, simOpts)

    def _runSim(self, dutName, simOpts):
        if simOpts:
            self.simulationOptions += simOpts;
        return call([self.VSIM]+self.simulationOptions+[dutName])
    


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
