# -*- coding: utf-8 -*-

from guietta import B, E, _, Gui, ___

# Compact definitions:
# Labels are just strings (now standard)
# A button is a string between square parenthesis (a 1-element sequence)
# an edit box is a string with double underscores

gui = Gui(
    
  [ 'Simulation:', ['On']      , ['Off'], 'sim_status' ],
  [ 'Position:'  , 'curpos'    , _      , 'moving'   ], 
  [ 'Move to:'   , '__newpos__', ___    , ['Move']   ] )

gui.run()

print('New position: ', gui.newpos.text())