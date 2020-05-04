# -*- coding: utf-8 -*-

from guietta import B, E, _, Gui

gui = Gui(
    
  [  _('Simulation'), B('On')    , B('Off'), _('sim_status') ],
  [  _('Position'),   _('curpos'), _       , _('moving')     ], 
  [  _('Move to:'),   E('usrpos'), _       , B('Move')       ] )

gui.run()


    