# -*- coding: utf-8 -*-

from guietta import B, _, Gui, Quit, Empty

counter = 0

gui = Gui(
    
  [  'Enter expression:', '__expr__'  , B('Eval!') ],
  [  'Result:'          , 'result'    , _          ],
  [  'counter'          , _           , Quit       ] )

while True:
    try:
        name, event = gui.get(timeout=0.1)
    except Empty:
        counter += 1
        gui.counter = counter
        continue

    if name == 'Eval':
        try:
            gui.result = eval(gui.expr)
        except Exception as e:
            gui.result = 'Error: ' + str(e)

    elif name is None:
        break
