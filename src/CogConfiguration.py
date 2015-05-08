import configparser
import pdb


class CogConfiguration(object):
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('conf.ini')

        self.TB_ENTITY = config.get('General', 'TB_ENTITY')
        self.COMPILE_OPTIONS = [x.strip() for x in config.get('General', 'COMPILE_OPTIONS').split(',')]
        self.SIM_OPTIONS = [x.strip() for x in config.get('General', 'SIM_OPTIONS').split(',')]
        self.BASEDIR = [x.strip() for x in config.get('Files', 'BASEDIR').split(',')]
        self.TB_FILE = config.get('Files', 'TB_FILE')
        
        # Implementation specifics
        try: self.MODELSIM = config.get('Files', 'MODELSIM')
        except: self.MODELSIM = None
