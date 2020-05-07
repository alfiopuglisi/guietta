# -*- coding: utf-8 -*-

import os.path
from guietta import B, L, _, Gui, Quit

gui = Gui(
    
  [  'Enter expression:', '__expr__'  , B('right.png', 'newname') ],
  [  L('left.png', 'result')          , 'result'    , _          ],
  [  _                  , _           , Quit       ],
  
  images_dir = os.path.dirname(__file__)
  
  )

while True:
    name, signal, *args = gui.get()
    print(name, signal, args)
    if name == 'newname':
        try:
            result = eval(gui.expr.text())
            gui.result.setText(str(result))
        except Exception as e:
            gui.result.setText('Error: '+str(e))

    elif name == None:
        break


