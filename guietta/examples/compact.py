# -*- coding: utf-8 -*-

from guietta import B, E, _, Gui, ___

gui = Gui(
    
  [ 'Simulation:', ['On']      , ['Off'], 'sim_status' ],
  [ 'Position:'  , 'curpos'    , _      , 'moving'   ], 
  [ 'Move to:'   , '__newpos__', ___    , ['Move']   ] )

gui.run()

print('New position: ', gui.newpos.text())