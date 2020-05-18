# -*- coding: utf-8 -*-

from guietta import _, ___, Gui, Quit, Exceptions, CB

def calculate(gui):
    name, op = gui.get_selections('op')
    result = getattr(float(gui.num1), op).__call__(float(gui.num2))
    gui.result = result

def change(gui):

    opdict = {'^' : '__pow__',
              '==': '__eq__',
              '>' : '__gt__',
              '//': '__floordiv__'}

    gui.op = opdict

def get(gui):
    print(gui.op)

    
opdict = {'+': '__add__',
          '-': '__sub__',
          '*': '__mul__',
          '/': '__truediv__'}

gui = Gui(
    
  [  'Enter numbers:', '__num1__' , CB('op', opdict) , '__num2__',  ['Calculate'] ],
  [  'Result:  -->'  , 'result'   ,       ___        ,  ___      ,   ['Change']   ],
  [  _               ,    _       ,        _         ,  ['Get']  ,      Quit      ],
  exceptions = Exceptions.POPUP)

gui.events(

    [  _             ,    _       ,  _  ,   _       ,    calculate   ],
    [  _             ,    _       ,  _  ,   _       ,    change      ],
    [  _             ,    _       ,  _  ,   get     ,    _           ] )


gui.run()
