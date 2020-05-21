# -*- coding: utf-8 -*-

from guietta import _, ___, Gui, Quit, Exceptions, slot

        
gui = Gui(
    
  [  'Enter numbers:', '__num1__' , '+' , '__num2__',  ['Calculate'] ],
  [  'Result:  -->'  , 'result'   , ___ ,  ___      ,  ['Calc2']     ],
  [  _               ,    _       ,  _  ,   _       ,      Quit      ],
  exceptions = Exceptions.POPUP)


@slot(gui.Calculate, gui.Calc2)
def calc(gui):
    gui.result = float(gui.num1) + float(gui.num2)


gui.run()
