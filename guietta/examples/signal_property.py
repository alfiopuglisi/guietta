# -*- coding: utf-8 -*-

# Demonstrates how to use Gui properties
# to connect a handler to a widget's default signal

from guietta import _, ___, Gui, Quit, Exceptions
        
gui = Gui(
    
  [  'Enter numbers:', '__num1__' , '+' , '__num2__',  ['Calculate'] ],
  [  'Result:  -->'  , 'result'   , ___ ,  ___      ,       _        ],
  [  _               ,    _       ,  _  ,   _       ,      Quit      ],
  exceptions = Exceptions.POPUP)


def calc(gui, *args):
    gui.result = float(gui.num1) + float(gui.num2)

# Assign a callable to the button

gui.Calculate = calc

gui.run()
