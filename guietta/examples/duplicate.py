# -*- coding: utf-8 -*-

from guietta import B,  _, Gui, Quit

gui = Gui(
    
  [  'Enter expression:', '__expr__'  , B('Eval!') ],
  [  'result'          , 'result'    , _          ],
  [  _                  , _           , Quit       ] )

while True:
    name, signal, *args = gui.get()

    if name == 'Eval':
        result = eval(gui.expr.text())
        gui.result.setText(str(result))

    if name == None:
        break


