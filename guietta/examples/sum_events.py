# -*- coding: utf-8 -*-

from guietta import _, ___, Gui, Quit

def calculate(gui):
    try:
        result = float(gui.num1.text()) + float(gui.num2.text())
    except Exception as e:
        result = 'Error: ' + str(e)
    gui.result.setText(str(result))
        
gui = Gui(
    
  [  'Enter numbers:', '__num1__' , '+' , '__num2__',  ['Calculate'] ],
  [  'Result:  -->'  , 'result'   , ___ ,  ___      ,       _        ],
  [  _               ,    _       ,  _  ,   _       ,      Quit      ] )

gui.events(

    [  _             ,    _       ,  _  ,   _       ,    calculate   ],
    [  _             ,    _       ,  _  ,   _       ,    _           ],
    [  _             ,    _       ,  _  ,   _       ,    _           ] )

gui.run()
