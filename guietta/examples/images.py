# -*- coding: utf-8 -*-

import os.path
from guietta import B, L, _, Gui

Gui.set_images_dir(os.path.dirname(__file__))

gui = Gui(
    
  [  _             , L('up.png')   , _              ],
  [  B('left.png') ,     _         , B('right.png') ],
  [  _             , L('down.png') , _           ,  ],

  )

gui.names(
    
  [  _    , _   , _     ],
  [ 'left', _   ,'right'],
  [ _     , _   , _     ],   
    
    )

while True:
    name, signal, *args = gui.get()

    print(name, signal, args)

    if name == None:
        break


