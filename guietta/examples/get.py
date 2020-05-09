# -*- coding: utf-8 -*-

from guietta import B,  _, Gui, Quit

gui = Gui(
    
  [  'Enter expression:', '__expr__'  , B('Eval!') ],
  [  'Result:'          , 'result'    , _          ],
  [  _                  , _           , Quit       ] )

while True:
    name, event = gui.get()

    if name == 'Eval':
        try:
            gui.result = eval(gui.expr)
        except Exception as e:
            gui.result = 'Error: ' + str(e)

    elif name == None:
        break


