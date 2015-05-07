#!/usr/bin/python3

import sys
import os
import subprocess
import shutil
import errno
import logging
import pdb

logging.basicConfig(level=logging.DEBUG)

if len(sys.argv) == 4:
    BASE_DIR_PATH = os.path.abspath(sys.argv[1])
    MODELSIM_PATH = os.path.abspath(sys.argv[3])
    TB_DIR_PATH =  os.path.abspath('.') + os.sep
    simDirPath = TB_DIR_PATH+os.sep+'sim'+os.sep
    # Assuming it's the same
    tbFileName = os.path.join(TB_DIR_PATH, sys.argv[2])
    tbEntity = '.'.join((sys.argv[2]).split('.')[0:-1])
elif len(sys.argv) == 1:
    BASE_DIR_PATH = os.path.abspath('..') + os.sep
    TB_DIR_PATH = None
    MODELSIM_PATH = '/cygdrive/e/modeltech_pe_10.4a/win32pe/'
    simDirPath = BASE_DIR_PATH+os.sep+'sim'+os.sep
    logging.warning('Using default settings; please check your conf.py file.')
    raise SystemExit('Not supported')
else:
    logging.warning('Unsupported number of settings')
    raise SystemExit

replacements = { '__MODELSIM_PATH__' : repr(MODELSIM_PATH) , '__TB_FILE__' : repr(tbFileName),
                 '__TB_ENTITY__' : repr(tbEntity)}
if TB_DIR_PATH:
    replacements.update({'__BASE_DIR_PATH__' : str([BASE_DIR_PATH, TB_DIR_PATH]) })
else:
    replacements.update({ '__BASE_DIR_PATH__' : str([BASE_DIR_PATH]) })
linkItems = [] 
copyItems = ['run.do', 'wave.do'] + ['simCompile.py', 'xsim.py']


################################################################################
# From http://code.activestate.com/lists/python-list/27163/
def force_symlink(file1, file2):
    if sys.platform == 'win32' and os.path.isdir(file1):
        subprocess.call(['cmd', '/c', 'mklink', '/J', file2, file1])
    try:
        os.symlink(file1, file2)
    except OSError as e:
        if e.errno == errno.EEXIST:
            os.remove(file2)
            os.symlink(file1, file2)
################################################################################
    
print("Setting up simulation folder: " + simDirPath)


try: os.mkdir(simDirPath)
except OSError : logging.debug('Folder already exists')

try:
    #os.chdir(simDirPath)
    pass
except OSError :
    logging.warning('Folder sim does not exist')
    raise SystemExit

cogDir = os.path.dirname(os.path.abspath(__file__))
pdb.set_trace()


with open(os.path.join(cogDir,'conf.tpl'), 'r') as srcFp:
    with open(simDirPath+'conf.py', 'w') as destFp:
        for line in srcFp:
            for src, target in replacements.items():
                line = line.replace(src, target)
            destFp.write(line)
            logging.debug(line)

force_symlink(cogDir, os.path.join(simDirPath, 'cog'))
for i in linkItems:
    force_symlink(os.path.join(cogDir, i), os.path.join(simDirPath, i))
for i in copyItems:
    shutil.copy(os.path.join(cogDir, i), os.path.join(simDirPath, i))
