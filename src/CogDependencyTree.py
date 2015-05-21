import os
import copy
import pdb
import logging

from .functions import str_fname_inode


PARSE_LOOP_ABORT_LIMIT = 10000


class CogDependencyTree(object):
    '''Generate the dependecies from a TreeWalker parsed tree.'''

    def __init__(self):
        self.parsed_tree = None
        self.top_file = None
        self.ignore_libs = []
        self.col = None


    def gen_dep_tree(self):
        assert self.parsed_tree != None

        if not self.top_file:
            self.col = self._generate_dependency_tree(self.parsed_tree)
        elif os.path.isfile(self.top_file):
            self.col = self._generate_dependency_file()
        else:
            raise Exception('File does not exist: ' + self.top_file)


    def _generate_dependency_tree(self, parsed_tree):
        iter_count = 0
        par_tree = copy.copy(parsed_tree)
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
            parsed_tree_subset[i] = self.parsed_tree[i]

        return self._generate_dependency_tree(parsed_tree_subset)


    def _sample_req_files(self, filename):
        abs_filename = os.path.abspath(filename)
        cur_inode_string = str_fname_inode(abs_filename)
        req_files = [cur_inode_string]

        for dep in self.parsed_tree[cur_inode_string]['deps']:
            if len(dep) > 0:
                ret = self._call_req_files_by_obj_name(dep)
                for i in ret:
                    try:
                        req_files.index(i)
                    except ValueError:
                        req_files.append(i)

        return req_files



    def _call_req_files_by_obj_name(self, dep):
        for key in self.parsed_tree:
            if not self.parsed_tree[key]['objName']:
                continue # No name in file.
            if ((self.parsed_tree[key]['lib'].lower() == dep[0] or dep[0] == None) and
                    self.parsed_tree[key]['objName'].lower() == dep[1]):
                return self._sample_req_files(self.parsed_tree[key]['path'])
        logging.warning('Not found ' + str(dep))
        return []
