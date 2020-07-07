# -*- coding: utf-8 -*-

from guietta import Gui, LB, _, III

def listbox(gui, text):
    print(text)

def test(gui, *args):
    print(gui.listbox)
    

gui = Gui(
    
  [ LB('listbox') ],
  [       III     ],
  [       III     ],
  [     ['Test']  ])


gui.events(
    
    [   listbox  ],
    [      _     ],
    [      _     ],
    [     test   ],
   )

gui.widgets['listbox'].setSelectionMode(gui.widgets['listbox'].ExtendedSelection)

gui.listbox = ['a', 'b', 'c', 'd']

gui.run()

    