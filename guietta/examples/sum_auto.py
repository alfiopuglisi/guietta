# -*- coding: utf-8 -*-

from guietta import _, ___, Gui, Quit, Exceptions
        
gui = Gui(
    
  [  'help'          , '__num1__' , '+' , '__num2__',   _    ],
  [  'Result:  -->'  , 'result'   , ___ ,  ___      ,   _    ],
  [  _               ,    _       ,  _  ,   _       ,  Quit  ],
  exceptions = Exceptions.POPUP)


@gui.auto
def calc(gui, *args):
    gui.result = float(gui.num1) + float(gui.num2)

gui.help=['Enter numbers','and press Enter -->']

gui.run()
