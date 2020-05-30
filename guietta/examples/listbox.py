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

from PySide2.QtWidgets import  QAbstractItemView
gui.widgets['listbox'].setSelectionMode(QAbstractItemView.ExtendedSelection)

gui.listbox = ['a', 'b', 'c', 'd']

gui.run()

    