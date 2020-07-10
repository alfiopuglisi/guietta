# -*- coding: utf-8 -*-

from guietta import _, ___, Gui, Quit, Exceptions


gui = Gui(
    
  [  'Enter numbers:', '__num1__' , '+' , '__num2__',  ['Calculate'] ],
  [  'Result:  -->'  , 'result'   , ___ ,  ___      ,       _        ],
  [  _               ,    _       ,  _  ,   _       ,      Quit      ],
  exceptions = Exceptions.POPUP,
  font = 'Comic Sans MS')

gui.fonts(

  [  _                   ,    _       ,  _  ,   _       ,    'Arial'   ],
  [  ('Helvetica', 12, 2),    _       ,  _  ,   _       ,       _      ],
  [  _                   ,    _       ,  _  ,   _       ,       _      ],
)


with gui.Calculate:
    gui.result = float(gui.num1) + float(gui.num2)
     
gui.run()
