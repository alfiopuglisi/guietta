# -*- coding: utf-8 -*-

import os.path
from guietta import B, L, _, Gui, Stretch

gui = Gui(
    
  [  _   , Stretch(2), _ ],
  [  _   , 'a'  , _   ],
  [  'b' ,  _   , 'd' ],
  [  _   , 'c'  , _   , Stretch(10)],
)

gui.window().resize(500,500)

while True:
    name, event = gui.get()

    print(name, event)

    if name == None:
        break


