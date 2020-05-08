# -*- coding: utf-8 -*-

import os.path
from guietta import Gui, _

# Labels and button automatically load images if the filename is valid,
# otherwise it will appear as text.
#
# Widget names are set to the image name without extension.

gui = Gui(
    
  [  _             , 'up.png'   , _             ],
  [  ['left.png'] ,     _       , ['right.png'] ],
  [  _             , 'down.png' , _             ],
  
    images_dir = os.path.dirname(__file__)

  )

while True:
    name, event = gui.get()

    if name == 'left':
        print('Clicked left!')

    if name == 'right':
        print('Clicked right!')

    if name == None:
        break


