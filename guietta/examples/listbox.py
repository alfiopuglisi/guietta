# -*- coding: utf-8 -*-

from guietta import Gui, LB, _, III
from qtpy.QtWidgets import QAbstractItemView

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

gui.widgets['listbox'].setSelectionMode(QAbstractItemView.ExtendedSelection)

gui.listbox = ['a', 'b', 'c', 'd']

gui.run()

    