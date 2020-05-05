# -*- coding: utf-8 -*-

from guietta import B, E, _, Gui

class Test(Gui):
    
    def __init__(self):
        super().__init__(        
    
  [  _('Simulation'), B('On')    , B('Off'), _('sim_status') ],
  [  _('Position'),   _('curpos'), _       , _('moving')     ], 
  [  _('Move to:'),   E('usrpos'),       _       , B('Move')       ] )

        self.events(

    [  _            , self.sim_on , self.sim_off, _       ],
    [  _            ,   _         , _           , _       ], 
    [  _            , self.move   , _           , self.move   ] )

    def sim_on(self):
        self.sim_status.setText('On')

    def sim_off(self):
        self.sim_status.setText('Off')

    def move(self):
        print('Moving to:'+ self.usrpos.text())


gui = Test()
gui.run()

