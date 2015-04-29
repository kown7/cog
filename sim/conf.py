import sys

BASEDIR = '../'
TB_FILE = BASEDIR + 'tb_test1.sv'

TB_ENTITY = 'TB_test1'
COMPILE_OPTIONS='+cover=sbceft'
SIM_OPTIONS='-coverage'

if sys.platform.startswith('cygwin'):
    # Cygwin
    MODELSIM = '/cygdrive/e/modeltech_pe_10.4a/win32pe/'
elif sys.platform.startswith('win'):
    # Win32
    MODELSIM = 'E:\\modeltech_pe_10.4a\\win32pe\\'

VLOG = MODELSIM + 'vlog.exe'
VCOM = MODELSIM + 'vcom.exe'
VLIB = MODELSIM + 'vlib.exe'
VSIM = MODELSIM + 'vsim.exe'
VDIR = MODELSIM + 'vdir.exe'
