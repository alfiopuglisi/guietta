# -*- coding: utf-8 -*-

from guietta import _, ___, Gui, Quit, Exceptions, CB


    
opdict = {'+': '__add__',
          '-': '__sub__',
          '*': '__mul__',
          '/': '__truediv__'}

gui = Gui(
    
  [  'Enter numbers:', '__num1__' , CB('op', opdict) , '__num2__',      _   ],
  [  'Result:  -->'  , 'result'   ,       ___        ,  ___      ,  ['Change'] ],
  [  _               ,    _       ,        _         ,  ['Get']  ,    Quit ],
  exceptions = Exceptions.OFF)


with gui.op:
    name, op = gui.get_selections('op')
    result = getattr(float(gui.num1), op).__call__(float(gui.num2))
    gui.result = result

with gui.Get:
    print('get')
    print(gui.op)

with gui.Change:
    if gui.is_running:
        opdict = {'^' : '__pow__',
                  '==': '__eq__',
                  '>' : '__gt__',
                  '//': '__floordiv__'}

        gui.op = opdict


gui.run()
