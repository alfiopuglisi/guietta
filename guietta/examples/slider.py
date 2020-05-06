# -*- coding: utf-8 -*-

from guietta import B, E, X, _, Gui, Quit
from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import Qt

def do_eval(gui):
    try:
        result = eval(gui.expr.text())
        gui.result.setText(str(result))
    except Exception as e:
        gui.result.setText('Error: '+str(e))

def do_slider(gui, state):
    gui.result.setText('%d' % state)

s = QSlider(Qt.Horizontal)

gui = Gui(
    
  [  'Enter expression:', E('expr')  , B('Eval!') ],
  [  'Result:'          , 'result'    , _          ],
  [  X(s, 'myslider')      , _        , Quit       ] )


gui.events(
    
    [  _            ,   do_eval   , do_eval    ], 
    [  _            ,   _         , _          ], 
    [  do_slider    ,   _         , _          ], )


gui.run()

# GUI widgets are available after window closing,
print(gui.result.text())

    