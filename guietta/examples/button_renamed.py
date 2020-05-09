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
    name, event = gui.get()
    print(name, event)
    if name == 'newname':
        try:
            gui.result = eval(gui.expr)
        except Exception as e:
            gui.result = 'Error: ' + str(e)

    elif name == None:
        break


