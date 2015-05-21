'''cog.py
Copyright (c) Kristoffer Nordstroem, All rights reserved.

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 3.0 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library.

------------------------------------------------------

Usage:
   In general the following:
    - setup config
    - load cache
    - load current compile times
    - TreeWalker parse
    - order list
    - compile
    - update compile times
    - store cache
    See also the runAll() function.

Compiler implementation need to implement the CogCompilerInterface
class.

The debug level needs to be set with the constructor
'''

import logging
import json
import os
import copy
import pdb

from .TreeWalker import TreeWalker
from .functions import str_fname_inode


PARSE_LOOP_ABORT_LIMIT = 10000


class Cog(object):
    '''Global compile-order-generator class. Manages the file-parser and
    list-generator

    '''
    def __init__(self, **kwargs):
        self.libs = []
        if kwargs.get('basedir'):
            self.libs.append({'basedir' : kwargs.get('basedir', os.path.expanduser('~')),
                              'lib' : kwargs.get('lib', 'work'),
                              ## Directories not to be parsed; relative path to basedir
                              'exclude' : kwargs.get('exclude', [])})
        # File path needs to absolute
        self.top_file = os.path.abspath(kwargs.get('top', ''))
        # Should not be None, as it may trigger weird behaviour
        self.ignore_libs = kwargs.get('ignoreLibs', [])
        self.debug = kwargs.get('debug', False)
        # col : compile order list
        self.col = []
        # Assign compiler object to have runAll fun.
        self.comp = None

        self._cache = None
        self._parsed_tree = {}
        self._cache_file = os.path.join(os.path.expanduser('~'), '.cog.py.stash')

        if self.debug:
            logging.basicConfig(level=logging.DEBUG)


    def add_lib(self, bdir, lib, exclude=None):
        if not exclude:
            exclude = []
        self.libs.append({'basedir' : bdir, 'lib' : lib, 'exclude' : exclude})


    def parse(self):
        for lib in self.libs:
            walked_tree = TreeWalker(lib['basedir'], lib['lib'], '', lib['exclude'], self._cache)
            self._parsed_tree.update(walked_tree.parse())


    def gen_tree_all(self):
        self.col = self._generate_dependency_tree(self._parsed_tree)


    def gen_tree_file(self, *args):
        if len(args) > 0:
            self.top_file = os.path.abspath(args[0])
        if os.path.isfile(self.top_file):
            self.col = self._generate_dependency_file()
        else:
            logging.error('File does not exist: ' + self.top_file)


    def load_cache(self):
        try:
            with open(self._cache_file, 'r') as file_handler:
                self._cache = json.load(file_handler)
        except IOError:
            self._cache = None
            logging.warning('Could not open cache file')


    def import_compile_times(self, designs):
        if not self._parsed_tree:
            raise Exception
        for inode in designs:
            if self._parsed_tree[inode]:
                try:
                    self._parsed_tree[inode].update({'ctime' : designs[inode]['ctime']})
                except KeyError:
                    logging.warning('No ctime found for ' + designs[inode]['name'])


    def save_cache(self):
        with open(self._cache_file, 'w') as file_handler:
            file_handler.write(json.dumps(self._cache))

    def print_csv(self):
        for obj in self.col:
            print(obj[0] + ',' + obj[1])

    def compile_all(self, force_compile=False):
        self.load_cache()
        self.parse()
        if not force_compile:
            self.import_compile_times(self.comp.getLibsContent(self.libs))
        self.gen_tree_all()
        self.comp.compileAllFiles(self.col)
        self.save_cache()


    def compile_file(self, force_compile=False):
        self.load_cache()
        self.parse()
        if not force_compile:
            self.import_compile_times(self.comp.getLibsContent(self.libs))
        self.gen_tree_file()
        self.comp.compileAllFiles(self.col)
        self.save_cache()



    def _generate_dependency_tree(self, parsed_tree_input):
        '''TODO: In order to prevent dependecies to be broken, we'd need to
        walk through the entire tree from both directions.

        '''
        iter_count = 0
        par_tree = copy.copy(parsed_tree_input)
        col = [] # compile order list
        col_ign = [] # dependencies not to be compiled
        col_fp = [] # compile order list with filenames instead

        while len(par_tree) > 0:
            for key in par_tree:
                if self._is_in_col(par_tree[key]['deps'], col_ign, par_tree):
                    if par_tree[key]['mtime'] < par_tree[key]['ctime']:
                        col_ign.append([par_tree[key]['lib'], par_tree[key]['objName']])
                    else:
                        col.append([par_tree[key]['lib'], par_tree[key]['objName']])
                        col_fp.append([par_tree[key]['lib'], par_tree[key]['path'], par_tree[key]['type']])
                    del par_tree[key]
                    break
                elif self._is_in_col(par_tree[key]['deps'], col, par_tree):
                    col.append([par_tree[key]['lib'], par_tree[key]['objName']])
                    col_fp.append([par_tree[key]['lib'], par_tree[key]['path'], par_tree[key]['type']])
                    del par_tree[key]
                    break
                elif self._is_in_col(par_tree[key]['deps'], col+col_ign, par_tree):
                    col.append([par_tree[key]['lib'], par_tree[key]['objName']])
                    col_fp.append([par_tree[key]['lib'], par_tree[key]['path'], par_tree[key]['type']])
                    del par_tree[key]
                    break

            if iter_count == PARSE_LOOP_ABORT_LIMIT:
                pdb.set_trace()
                raise Exception
            else:
                iter_count += 1

        return col_fp



    def _is_in_col(self, deps, col, parsed_tree):
        for dep in deps:
            try:
                self.ignore_libs.index(dep[0])
                continue # next element
            except ValueError:
                pass

            try:
                # Assume if library is not given, that it's a VHDL file
                # with default library 'work'
                if dep[0] == None:
                    col.index(['work', dep[1]])
                else:
                    col.index(dep)
            except ValueError:
                if dep[0] == None and self._is_in_tree(dep[1], parsed_tree) == False:
                    pass
                else:
                    return False
        return True


    def _is_in_tree(self, entity, parsed_tree):
        for key in parsed_tree:
            if parsed_tree[key]['objName'].lower() == entity:
                if parsed_tree[key]['lib'].lower() != 'work':
                    logging.warning('Object ' + entity + ' found in library ' + parsed_tree[key]['lib'])
                return True
        return False



    def _generate_dependency_file(self):
        abs_filename = os.path.abspath(self.top_file)
        parsed_tree_subset = {}

        req_files = self._sample_req_files(abs_filename)

        for i in req_files:
            parsed_tree_subset[i] = self._parsed_tree[i]

        return self._generate_dependency_tree(parsed_tree_subset)


    def _sample_req_files(self, filename):
        abs_filename = os.path.abspath(filename)
        cur_inode_string = str_fname_inode(abs_filename)
        req_files = [cur_inode_string]

        for dep in self._parsed_tree[cur_inode_string]['deps']:
            if len(dep) > 0:
                ret = self._call_req_files_by_obj_name(dep)
                for i in ret:
                    try:
                        req_files.index(i)
                    except ValueError:
                        req_files.append(i)

        return req_files



    def _call_req_files_by_obj_name(self, dep):
        for key in self._parsed_tree:
            if not self._parsed_tree[key]['objName']:
                continue # No name in file.
            if ((self._parsed_tree[key]['lib'].lower() == dep[0] or dep[0] == None) and
                    self._parsed_tree[key]['objName'].lower() == dep[1]):
                return self._sample_req_files(self._parsed_tree[key]['path'])
        logging.warning('Not found ' + str(dep))
        return []
