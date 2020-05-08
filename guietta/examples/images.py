# -*- coding: utf-8 -*-

import os.path
from guietta import B, L, _, Gui

gui = Gui(
    
  [  _             , L('up.png')   , _              ],
  [  B('left.png') ,     _         , B('right.png') ],
  [  _             , L('down.png') , _           ,  ],

  images_dir = os.path.dirname(__file__))

while True:
    name, event = gui.get()

    print(name, event)

    if name == None:
        break


