# -*- coding: utf-8 -*-

from guietta import B, E, _, Gui

def sim_on(gui):
    gui.sim_status.setText('On')

def sim_off(gui):
    gui.sim_status.setText('Off')

def move(gui):
    print('Moving to:'+ gui.usrpos.text())


class Test(Gui):
    
    def __init__(self):
        super().__init__(        
    
  [  'Simulation', B('On')     , B('Off'),   'sim_status' ],
  [  'Position'  ,   'curpos'  , _       ,   'moving'     ], 
  [  'Move to:'  , E('usrpos') , _       , B('Move')      ] )

        self.events(

    [  _            , sim_on , sim_off, _       ],
    [  _            ,   _    , _      , _       ], 
    [  _            , move   , _      , move   ] )


gui = Test()
gui.run()

