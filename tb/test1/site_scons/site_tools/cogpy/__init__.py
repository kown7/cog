"""SCons.Tool.cogpy

Copyright (c) 2015 K. Nordstroem <k.nordstroem@helveting.ch>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

"""

import SCons.Action
import SCons.Builder
import SCons.Util

import pdb
import subprocess
import os
from cog import CogEnv


def _cog_py_builder(target, source, env):
    env['COG_INST'].compile_file()
    return None

    
_cogpy_action_builder = SCons.Builder.Builder(
        action = _cog_py_builder,
        suffix = '',
        src_suffix = ['.sv', '.vhdl']
        )

     
def _cog_py_sim(target, source, env):
    env['COG_INST'].cfg._sim_options += ['-do', 'sim'+os.path.sep+'run.do']
    env['COG_INST'].run_simulation()
    # There is no parsing of the simulation output.
    return None

    
_cogpy_action_sim = SCons.Builder.Builder(
    action = _cog_py_sim,
    suffix = '',
    src_suffix = ['.do']
)


def _ensure_path(path):
    if os.sys.platform == 'cygwin' and path:
        if len(path[0]) == 1:
            args = ['cygpath.exe', '-u', path]
            conv_path = subprocess.check_output(args).strip()
        else:
            conv_path = []
            for i in path:
                args = ['cygpath.exe', '-u', i]
                conv_path.append(subprocess.check_output(args).strip())
    else:
        conv_path = path
    return conv_path

def generate(env):
    env['COG_INST'] = CogEnv()
    env['COG_INST'].cfg._tb_entity = _ensure_path(env['TB_ENTITY'])
    env['COG_INST'].cfg._compile_options = env['COMPILE_OPTIONS']
    env['COG_INST'].cfg._sim_options = env['SIM_OPTIONS']
    env['COG_INST'].cfg._basedir = _ensure_path(env['BASEDIR'])
    env['COG_INST'].cfg._tb_file = _ensure_path(env['TB_FILE'])
    env['COG_INST'].cfg._modelsim = _ensure_path(env['MODELSIM'])
    env['COG_INST'].force_compile = True
    env['COG_INST'].factory()

    env['BUILDERS']['cogpy_builder'] = _cogpy_action_builder # _cog_py_builder
    env['BUILDERS']['cogpy_sim'] = _cogpy_action_sim

def exists(env):
    return None
