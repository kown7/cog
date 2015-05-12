# cog

Compile Order Generator for VHDL written in Python. Now also with
limited support for SystemVerilog, i.e., it only supports one instance which is
expected to be the DUT, whose name must start with 'i_'.


The exmaple-tool branch should work as an example. I try to create a small
documentation here.


Example file tree setup:
 /
  ./src/   contains source files
        test1.vhd   DUT
  ./tb
      ./test1   One test case
         ...
      ./testn   Nth test case
      ./cog     master branch cog checkout


Runnig the createSimFolder.py script in the respective testx folder will create
a subfolder testn/sim.  Therein will the respective cog scripts be copied. It
is important though to run createSimFolder.py in the testx folder. Under
windows, e.g.:

$ cd /tb/test1
$ ../cog/createSimFolder.py ..\..\src tb_test1.sv E:\modeltech_pe_10.4a\win32pe\
$ ./sim/xsim.py

to start the modelsim GUI.

