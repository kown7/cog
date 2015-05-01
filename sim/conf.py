import sys

TB_ENTITY = 'TB_test1'
COMPILE_OPTIONS=['+cover=sbceft']
SIM_OPTIONS=['-coverage', '-msgmode', 'both', '-displaymsgmode', 'both']

if sys.platform.startswith('cygwin'):
    # Cygwin
    MODELSIM = '/cygdrive/e/modeltech_pe_10.4a/win32pe/'
    BASEDIR =  '../'
elif sys.platform.startswith('win'):
    # Win32
    MODELSIM = 'E:\\modeltech_pe_10.4a\\win32pe\\'
    BASEDIR = 'C:\\Users\\kn\\Documents\\workspace\\test1\\'

TB_FILE = BASEDIR + 'tb_test1.sv'
