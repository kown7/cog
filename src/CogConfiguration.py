import configparser
import os

class CogConfiguration(object):
    def __init__(self):
        self._tb_entity = ''
        self._compile_options = []
        self._sim_options = []
        self._basedir = []
        self._tb_file = ''
        self._modelsim = None

        if os.path.isfile('conf.ini'):
            config = configparser.ConfigParser()
            config.read('conf.ini')

            self._tb_entity = config.get('General', 'TB_ENTITY')
            self._compile_options = [x.strip()
                                     for x in config.get('General', 'COMPILE_OPTIONS').split(',')]
            self._sim_options = [x.strip()
                                 for x in config.get('General', 'SIM_OPTIONS').split(',')]
            self._basedir = [x.strip() for x in config.get('Files', 'BASEDIR').split(',')]
            self._tb_file = config.get('Files', 'TB_FILE')

            # Implementation specifics
            try:
                self._modelsim = config.get('Files', 'MODELSIM')
            except (NoOptionError, NoSectionError):
                self._modelsim = None

    @property
    def TB_ENTITY(self):
        return self._tb_entity

    @property
    def COMPILE_OPTIONS(self):
        return self._compile_options

    @property
    def SIM_OPTIONS(self):
        return self._sim_options

    @property
    def BASEDIR(self):
        return self._basedir

    @property
    def TB_FILE(self):
        return self._tb_file

    @property 
    def MODELSIM(self):
        return self._modelsim
