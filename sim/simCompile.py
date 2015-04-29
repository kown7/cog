#!/usr/bin/python3

from cog import *
from conf import *

from subprocess import call, check_output
import sys
import os
import re

from datetime import datetime
import time
import pprint


def splitStringIter(foobar): return iter(foobar.splitlines())


def modelsimCompensateOffset():
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


def modelsimCompile(f):
        lenv=modelsimCompensateOffset()

        for fp in f.col:
                if fp[2] == cog.CogFileType.VhdlEntity or fp[2] == cog.CogFileType.VhdlPackage:
                        compiler = VCOM
                if fp[2] == cog.CogFileType.SvModule:
                        compiler = VLOG


                parms = [compiler, COMPILE_OPTIONS, '-work', fp[0],fp[1]]
                call(parms, env=lenv)


def modelsimLibParsed(curLib = 'work'):
        lenv=modelsimCompensateOffset()
        try:
                libContent = check_output([VDIR, '-l', '-lib', curLib], env=lenv)
        except:
                print(VDIR)
                print(libContent)
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
                        # Ignoring locale, assuming en_US. Will cause troubles
                        cTime = datetime.strptime(m.group(1) + ' GMT', '%a %b %d %X %Y %Z')
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


def simCompile():
        os.chdir(BASEDIR+'sim'+os.sep)
        print(os.getcwd())

        try:
                sys.argv.index('-f')
                libContent = []
        except:
                libContent = modelsimLibParsed()

        #f = cog.cog( basedir=BASEDIR, top=TB_FILE, debug=1 )
        f = cog.cog( basedir=BASEDIR, top=TB_FILE )
        f.loadCache()
        f.parse()
        f.importCompileTimes(libContent)
        f.genTreeAll()

        modelsimCompile(f)

        f.saveCache()

simCompile()
