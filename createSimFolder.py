#!/usr/bin/python3

import sys
import os
import subprocess
import shutil
import errno
import logging
#import pdb

logging.basicConfig(level=logging.DEBUG)

def help_message():
    print('Usage: setup.py <src directory> <top file> <modelsim bin path>\n' +
          '\t<top file>:\tis assumed to be in a different directory;\n' +
          '\t\t\tmay contain more files.\n')


try:
    sys.argv.index('-h')
except ValueError:
    pass
else:
    help_message()
    raise SystemExit('All help there is!')

if len(sys.argv) == 4:
    BASE_DIR_PATH = os.path.abspath(sys.argv[1])
    MODELSIM_PATH = os.path.abspath(sys.argv[3])
    TB_DIR_PATH = os.path.abspath('.') + os.sep
    SIM_DIR_PATH = os.path.join(TB_DIR_PATH, 'sim')
    # Assuming it's the same
    TB_FILENAME = os.path.join(TB_DIR_PATH, sys.argv[2])
    TB_ENTITY = '.'.join((sys.argv[2]).split('.')[0:-1])
else:
    raise SystemExit('Unsupported number of params')

REPLACEMENTS = {'__MODELSIM_PATH__' : MODELSIM_PATH, '__TB_FILE__' : TB_FILENAME,
                '__TB_ENTITY__' : TB_ENTITY}
if TB_DIR_PATH:
    # TB_DIR_PATH is first, because simCompile uses the first
    # entry+sim as the compile-location.
    REPLACEMENTS.update({'__BASE_DIR_PATH__' : ','.join([TB_DIR_PATH, BASE_DIR_PATH])})
else:
    REPLACEMENTS.update({'__BASE_DIR_PATH__' : ','.join([BASE_DIR_PATH])})

REPLACE_ITEMS = (('conf.tpl', 'conf.ini'), ('wave.tpl', 'wave.do'))
LINK_ITEMS = [] # Windows again
COPY_ITEMS = ['run.do'] + ['simCompile.py', 'xsim.py', 'sim.py']

COG_DIR = os.path.dirname(os.path.abspath(__file__))
COG_TPL_DIR = os.path.join(COG_DIR, 'tpl')

################################################################################
# From http://code.activestate.com/lists/python-list/27163/
def force_symlink(file1, file2):
    if sys.platform == 'win32':
        if os.path.isdir(file1):
            try:
                subprocess.check_output(['cmd', '/c', 'mklink', '/J', file2, file1],
                                        stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as cpe:
                if cpe.returncode == 1:
                    logging.debug('Most likely, the link already existed: '+
                                  cpe.output.decode('utf-8').strip())
                else:
                    logging.warning('mklink failed: '+cpe.output.decode('utf-8').strip())
        else:
            raise Exception('Not supported in win due to security settings.')
    else:
        try:
            os.symlink(file1, file2)
        except OSError as errtype:
            if errtype.errno == errno.EEXIST:
                os.remove(file2)
                os.symlink(file1, file2)
################################################################################

print("Simulation dir: " + SIM_DIR_PATH)


try:
    os.mkdir(SIM_DIR_PATH)
except OSError:
    logging.debug('Folder already exists')


force_symlink(COG_DIR, os.path.join(SIM_DIR_PATH, 'cog'))
#pdb.set_trace()

for src, dest in REPLACE_ITEMS:
    with open(os.path.join(COG_TPL_DIR, src), 'r') as srcFp:
        with open(os.path.join(SIM_DIR_PATH, dest), 'w') as destFp:
            for line in srcFp:
                for src, target in REPLACEMENTS.items():
                    line = line.replace(src, target)
                destFp.write(line)
                logging.debug(line.strip())

for i in LINK_ITEMS:
    force_symlink(os.path.join(COG_TPL_DIR, i), os.path.join(SIM_DIR_PATH, i))
for i in COPY_ITEMS:
    shutil.copy(os.path.join(COG_TPL_DIR, i), os.path.join(SIM_DIR_PATH, i))
