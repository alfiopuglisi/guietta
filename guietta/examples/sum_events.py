# -*- coding: utf-8 -*-

from guietta import _, ___, Gui, Quit, Exceptions

def calculate(gui, *args):
    result = float(gui.num1) + float(gui.num2)
    gui.result = result
        
gui = Gui(
    
  [  'Enter numbers:', '__num1__' , '+' , '__num2__',  ['Calculate'] ],
  [  'Result:  -->'  , 'result'   , ___ ,  ___      ,       _        ],
  [  _               ,    _       ,  _  ,   _       ,      Quit      ],
  exceptions = Exceptions.POPUP)

gui.events(

    [  _             ,    _       ,  _  ,   _       ,    calculate   ],
    [  _             ,    _       ,  _  ,   _       ,    _           ],
    [  _             ,    _       ,  _  ,   _       ,    _           ] )

gui.run()
