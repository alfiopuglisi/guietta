# -*- coding: utf-8 -*-

from guietta import _, ___, Gui, Quit

gui = Gui(
    
  [  'Enter numbers:', '__num1__' , '+' , '__num2__',  ['Calculate'] ],
  [  'Result:  -->'  , 'result'   , ___ ,  ___      ,       _        ],
  [  _               ,    _       ,  _  ,   _       ,      Quit      ] )

while True:
    name, event = gui.get()

    if name == 'Calculate':
        try:
            result = float(gui.num1.text()) + float(gui.num2.text())
        except Exception as e:
            result = 'Error: ' + str(e)

        gui.result.setText(str(result))

    elif name is None:
        break
