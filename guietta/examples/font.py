# -*- coding: utf-8 -*-

from guietta import _, ___, Gui, Quit, Exceptions


gui = Gui(
    
  [  'Enter numbers:', '__num1__' , '+' , '__num2__',  ['Calculate'] ],
  [  'Result:  -->'  , 'result'   , ___ ,  ___      ,       _        ],
  [  _               ,    _       ,  _  ,   _       ,      Quit      ],
  exceptions = Exceptions.POPUP)


      
from PySide2.QtGui import QFont

gui.window().setFont(QFont("Helvetica", pointSize = 12, weight=2, italic=True))

gui.widgets['Calculate'].setFont(QFont("Comic Sans MS", weight=5))

with gui.Calculate:
    gui.result = float(gui.num1) + float(gui.num2)
     
gui.run()
