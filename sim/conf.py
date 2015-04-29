import sys

TB_ENTITY = 'TB_test1'
COMPILE_OPTIONS='+cover=sbceft'
SIM_OPTIONS='-coverage'

if sys.platform.startswith('cygwin'):
    # Cygwin
    MODELSIM = '/cygdrive/e/modeltech_pe_10.4a/win32pe/'
    BASEDIR =  '/cygdrive/c/Users/kn/Documents/workspace/test1/'
elif sys.platform.startswith('win'):
    # Win32
    MODELSIM = 'E:\\modeltech_pe_10.4a\\win32pe\\'
    BASEDIR = 'C:\\Users\\kn\\Documents\\workspace\\test1\\'


TB_FILE = BASEDIR + 'tb_test1.sv'

VLOG = MODELSIM + 'vlog.exe'
VCOM = MODELSIM + 'vcom.exe'
VLIB = MODELSIM + 'vlib.exe'
VSIM = MODELSIM + 'vsim.exe'
VDIR = MODELSIM + 'vdir.exe'
