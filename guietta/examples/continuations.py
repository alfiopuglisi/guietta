# -*- coding: utf-8 -*-

import sys
from guietta import Gui, ___, III

if len(sys.argv) < 2:

    gui = Gui(
        
      [ 'Big label', ___  , 'xxx'],
      [     III    , III  , 'xxx'],
      [    'xxx'   ,'xxx'  , 'xxx'],
      )

elif sys.argv[1] == 'row':

     # This one will cause an exception because of ___ at the beginnng
     # of a row
     
     gui = Gui(
        
         [ 'xxx' , 'xxx' , 'xxx'],
         [  ___  ,  III  , 'xxx'],
         [ 'xxx' , 'xxx' , 'xxx'],
    )

elif sys.argv[1] == 'col':

     # This one will cause an exception because of III at the beginning
     # of a column
     
     gui = Gui(
        
         [ 'xxx' ,  III  , 'xxx'],
         [ 'xxx' , 'xxx' , 'xxx'],
         [ 'xxx' , 'xxx' , 'xxx'],
     )

else:
    print('Use no arguments or one of "row" or "col"')
    sys.exit(-1)

while True:
    name, event = gui.get()

    if name is None:
        break


