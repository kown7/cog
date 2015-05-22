import os

from .CogFileType import CogFileType


class FileHandler(object):
    def __init__(self, path, filename, lib):
        self.path = path
        self.filename = filename
        self.lib = lib
        self.file_path = os.path.join(path, filename)

        self.object_name = None
        self.object_type = CogFileType.Undefined
        self.library = 'work'
        self.st_mtime = 0
        self.compile_time = 0
        self.depends_on_object = []
        # Set to false if compile time and modification time has not
        # changed since last run.
        self.modified = True

        self._set_change_time()
        self._set_compile_time()

    def _set_change_time(self):
        stats = os.stat(self.file_path)
        self.st_mtime = stats.st_mtime

    def _set_compile_time(self):
        pass

    def get_info(self):
        # ctime : compile time
        return {'path' : self.file_path, 'objName' : self.object_name,
                'lib' : self.library, 'deps' : self.depends_on_object,
                'modified' : self.modified, 'mtime' : self.st_mtime,
                'ctime' : self.compile_time, 'type' : self.object_type}
