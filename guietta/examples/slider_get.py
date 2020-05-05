# -*- coding: utf-8 -*-

from guietta import B, E, X, _, Gui, Quit
from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import Qt


s = QSlider(Qt.Horizontal)

gui = Gui(
    
  [  'Enter expression:', E('expr')  , B('Eval!') ],
  [  'Result:'          , 'result'    , _          ],
  [  X(s, 'myslider')      , _        , Quit       ] )


while True:
    name, signal, *args = gui.get()

    if name == 'Eval':
        result = eval(gui.expr.text())
        gui.result.setText(str(result))
    
    if name == 'myslider':
        gui.result.setText(str(args[0]))

    elif name == None:
        break