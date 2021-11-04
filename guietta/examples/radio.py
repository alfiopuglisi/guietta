# -*- coding: utf-8 -*-

# Create three radio button groups and connect them
# in three different ways.

from guietta import Gui, _, R1, R2, R3

gui = Gui(

  [ R1('rad1',1),  R2('rad3')  , R3('rad5')   ],
  [ R1('rad2')  ,  R2('rad4')  , R3('rad6')   ],

)

def msg(gui, *args):
    print('second button group')

def event(gui, *args):
    print('third group')

gui.events(
    
   [   _        ,       _      ,   event   ],
   [   _        ,       _      ,   event   ],
   
)

with gui.rad1, gui.rad2:
    print('First button group')
    print('rad1 isChecked = ', gui.rad1.isChecked())
    print('rad2 isChecked = ', gui.rad2.isChecked())
    
gui.rad3 = msg
gui.rad4 = msg

gui.run()
