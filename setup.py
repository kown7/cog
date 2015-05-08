#!/usr/bin/python3

import sys
import os
import subprocess
import shutil
import errno
import logging
import pdb

logging.basicConfig(level=logging.DEBUG)

def helpMessage():
    print('Usage: setup.py <src directory> <top file> <modelsim bin path>\n' + 
          '\t<top file>:\tis assumed to be in a different directory;\n' +
          '\t\t\tmay contain more files.\n')


try:
    sys.argv.index('-h')
except:
    pass
else:
    helpMessage()
    raise SystemExit('All help there is!')

if len(sys.argv) == 4:
    BASE_DIR_PATH = os.path.abspath(sys.argv[1])
    MODELSIM_PATH = os.path.abspath(sys.argv[3])
    TB_DIR_PATH =  os.path.abspath('.') + os.sep
    simDirPath = TB_DIR_PATH+os.sep+'sim'+os.sep
    # Assuming it's the same
    tbFileName = os.path.join(TB_DIR_PATH, sys.argv[2])
    tbEntity = '.'.join((sys.argv[2]).split('.')[0:-1])
else:
    message = 'Unsupported number of params'
    raise SystemExit(message)

replacements = { '__MODELSIM_PATH__' : MODELSIM_PATH , '__TB_FILE__' : tbFileName,
                 '__TB_ENTITY__' : tbEntity}
if TB_DIR_PATH:
    # TB_DIR_PATH is first, because simCompile uses the first
    # entry+sim as the compile-location.
    replacements.update({'__BASE_DIR_PATH__' : ','.join([TB_DIR_PATH, BASE_DIR_PATH]) })
else:
    replacements.update({ '__BASE_DIR_PATH__' : ','.join([BASE_DIR_PATH]) })

replaceItems = (('conf.tpl','conf.ini'),('wave.tpl','wave.do'))
linkItems = [] # Windows again
copyItems = ['run.do'] + ['simCompile.py', 'xsim.py', 'sim.py'] 


################################################################################
# From http://code.activestate.com/lists/python-list/27163/
def force_symlink(file1, file2):
    if sys.platform == 'win32':
        if os.path.isdir(file1):
            subprocess.call(['cmd', '/c', 'mklink', '/J', file2, file1])
        else:
            raise Exception('Not supported in win due to security settings.')
    else:
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

cogDir = os.path.dirname(os.path.abspath(__file__))
#pdb.set_trace()

for src, dest in replaceItems:
    with open(os.path.join(cogDir,src), 'r') as srcFp:
        with open(os.path.join(simDirPath,dest), 'w') as destFp:
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
