# -*- coding: utf-8 -*-

from guietta import B, E, _, Gui

gui = Gui(
    
  [  'Simulation', B('On')     , B('Off'),   'sim_status' ],
  [  'Position'  ,   'curpos'  , _       ,   'moving'     ], 
  [  'Move to:'  , E('usrpos') , _       , B('Move')      ] )

gui.run()


    