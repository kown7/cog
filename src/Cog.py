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

col : compile-order-list
'''

import logging
import json
import os

from .TreeWalker import TreeWalker
from .CogDependencyTree import CogDependencyTree


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


    def import_compile_times(self, designs):
        if not self._parsed_tree:
            raise Exception
        for inode in designs:
            if self._parsed_tree[inode]:
                try:
                    self._parsed_tree[inode].update({'ctime' : designs[inode]['ctime']})
                except KeyError:
                    logging.warning('No ctime found for ' + designs[inode]['name'])


    def load_cache(self):
        try:
            with open(self._cache_file, 'r') as file_handler:
                self._cache = json.load(file_handler)
        except IOError:
            self._cache = None
            logging.warning('Could not open cache file')


    def save_cache(self):
        with open(self._cache_file, 'w') as file_handler:
            file_handler.write(json.dumps(self._cache))


    def gen_tree(self, *args):
        dep_tree = CogDependencyTree()
        dep_tree.parsed_tree = self._parsed_tree
        dep_tree.ignore_libs = self.ignore_libs

        if len(args) > 0:
            dep_tree.top_file = os.path.abspath(args[0])
        elif self.top_file:
            dep_tree.top_file = self.top_file
        else:
            dep_tree.top_file = None

        dep_tree.gen_dep_tree()
        self.col = dep_tree.col


    def print_csv(self):
        for obj in self.col:
            print(obj[0] + ',' + obj[1])
