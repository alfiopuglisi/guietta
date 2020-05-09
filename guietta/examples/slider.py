# -*- coding: utf-8 -*-

from guietta import B, E, _, Gui, Quit
from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import Qt

def do_eval(gui, *args):
    gui.result = eval(gui.expr)
 
def do_slider(gui, state):
    gui.result = '%d' % state

s = QSlider(Qt.Horizontal)

gui = Gui(
    
  [  'Enter expression:', E('expr')  , B('Eval!') ],
  [  'Result:'          , 'result'    , _          ],
  [  (s, 'myslider')      , _        , Quit       ] )


gui.events(
    
    [  _            ,   do_eval   , do_eval    ], 
    [  _            ,   _         , _          ], 
    [  do_slider    ,   _         , _          ], )


gui.run()

# GUI widgets are available after window closing,
print(gui.result)

    