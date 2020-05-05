# -*- coding: utf-8 -*-

from guietta import B, E, _, Gui

gui = Gui(
    
  [ 'Simulation:', ['On']      , ['Off'], 'sim_status' ],
  [ 'Position:'  , 'curpos'    , _      , 'moving'   ], 
  [ 'Move to:'   , '__newpos__', _      , ['Move']   ] )

gui.run()


    