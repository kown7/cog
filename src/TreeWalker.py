''' cog.py
Copyright (c) Kristoffer Nordström, All rights reserved.

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
'''

import os
import logging

from .VhdlFileHandler import VhdlFileHandler
from .SvFileHandler import SvFileHandler

class TreeWalker(object):
    def __init__(self, basedir, lib, path, exclude, cached):
        self.basedir = basedir
        self.lib = lib
        self.path = path
        self.exclude = exclude
        self.cpath = os.path.join(basedir, path)
        self.lsfiles = os.listdir(self.cpath)
        self.centries = {}
        self.cached = cached

        logging.debug(self.lsfiles)


    def _return_values(self):
        return self.centries


    def _parse_current_path(self):
        for i in self.lsfiles:
            cur_path = os.path.join(self.cpath, i)
            cur_stat = os.stat(cur_path)
            inode_idx = str(cur_stat.st_ino)
            logging.debug(i + ": " + str(cur_stat.st_mtime))
            if os.path.isdir(cur_path):
                cur_path_tw = TreeWalker(self.basedir, self.lib, os.path.join(self.path, i),
                                         self.exclude, self.cached)
                self.centries.update(cur_path_tw.parse())
            elif i.lower().endswith(('.vhd', '.vhdl')):
                try:
                    if (self.cached[inode_idx]['path'] == cur_path and
                            self.cached[inode_idx]['mtime'] == cur_stat.st_mtime):
                        self.centries[inode_idx] = self.cached[inode_idx]
                        self.centries[inode_idx]['modified'] = False
                    else:
                        raise Exception
                except (KeyError, TypeError):
                    logging.debug('VHDL file parsing: ' + i)
                    vhdl_inst = VhdlFileHandler(self.cpath, i, self.lib)
                    vhdl_inst.parse()
                    self.centries.update({str(cur_stat.st_ino) : vhdl_inst.getInfo()})
            elif i.lower().endswith(('.sv')):
                try:
                    if (self.cached[inode_idx]['path'] == cur_path and
                            self.cached[inode_idx]['mtime'] == cur_stat.st_mtime):
                        self.centries[inode_idx] = self.cached[inode_idx]
                        self.centries[inode_idx]['modified'] = False
                    else:
                        raise Exception
                except (KeyError, TypeError):
                    logging.debug('SystemVerilog file parsing: ' + i)
                    svinst = SvFileHandler(self.cpath, i, self.lib)
                    svinst.parse()
                    self.centries.update({str(cur_stat.st_ino) : svinst.getInfo()})


    def parse(self):
        try:
            self.exclude.index(self.path)
            return []
        except ValueError:
            pass

        self._parse_current_path()
        return self._return_values()
