# -*- coding: utf-8 -*-

from guietta import B, E, _, Gui

def sim_on(gui):
    print('you clicked sim_on')

def sim_off(gui):
    print('you clicked sim_off')

def move(gui):
    print('you clicked move')
    print(gui.usrpos.text())

gui = Gui(
    
  [  'Simulation', B('On')     , B('Off'),   'sim_status' ],
  [  'Position'  ,   'curpos'  , _       ,   'moving'     ], 
  [  'Move to:'  , E('usrpos') , _       , B('Move')      ] )


gui.events(
    
    [  _            , sim_on      , sim_off, _       ],
    [  _            ,   _         , _      , _       ], 
    [  _            , move        , _      , move   ] )


gui.run()

# GUI widgets are available after window closing,
print(gui.usrpos.text())

    