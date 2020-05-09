# -*- coding: utf-8 -*-

from guietta import _, ___, Gui, Quit

gui = Gui(
    
  [  'Enter numbers:', '__num1__' , '+' , '__num2__',  ['Calculate'] ],
  [  'Result:  -->'  , 'result'   , ___ ,  ___      ,       _        ],
  [  _               ,    _       ,  _  ,   _       ,      Quit      ] )

while True:
    name, event = gui.get()

    if name == 'Calculate':
        gui.result = float(gui.num1) + float(gui.num2)

    elif name is None:
        break
