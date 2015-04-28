#!/usr/bin/python3

from cog import cog
from subprocess import call

from conf import *

def simCompile(): 
        #f = cog.cog( basedir=BASEDIR, top=TB_FILE, debug=1 )
        f = cog.cog( basedir=BASEDIR, top=TB_FILE )
        
        f.loadCache()
        f.parse()
        f.genTreeAll()
        
        f.saveCache()
        
        for fp in f.col:
        	if fp[2] == 1 or fp[2] == 2:
        		parms = [VCOM, '-work', fp[0], fp[1]]
        	if fp[2] == 3:
        		parms = [VLOG, '-work', fp[0], fp[1]]
        
        	call(parms)

simCompile()

