import sys

TB_ENTITY = __TB_ENTITY__
COMPILE_OPTIONS=['+cover=sbceft']
SIM_OPTIONS=['-coverage', '-msgmode', 'both', '-displaymsgmode', 'both']

MODELSIM = __MODELSIM_PATH__
BASEDIR = __BASE_DIR_PATH__

TB_FILE = __TB_FILE__

#if sys.platform.startswith('cygwin'):
#    # Cygwin
#    MODELSIM = '/cygdrive/e/modeltech_pe_10.4a/win32pe/'
#    BASEDIR =  '../'
#elif sys.platform.startswith('win'):
#    # Win32
#    MODELSIM = 'E:\\modeltech_pe_10.4a\\win32pe\\'
#    BASEDIR = 'C:\\Users\\kn\\Documents\\workspace\\test1\\'
#
#TB_FILE = BASEDIR + 'tb_test1.sv'
