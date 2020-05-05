# -*- coding: utf-8 -*-

from guietta import B,  _, Gui, Quit

gui = Gui(
    
  [  'Enter expression:', '__expr__'  , B('Eval!') ],
  [  'Result:'          , 'result'    , _          ],
  [  _                  , _           , Quit       ] )

while True:
    name, signal = gui.get()

    if name == 'Eval':
        result = eval(gui.expr.text())
        gui.result.setText(str(result))

    elif name == None:
        break


