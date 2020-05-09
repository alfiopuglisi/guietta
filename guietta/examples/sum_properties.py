# -*- coding: utf-8 -*-

from guietta import _, ___, Gui, Quit, HS

gui = Gui(
    
  [  'Enter numbers:', '__num1__' , '+' , '__num2__'  ,  ['Calculate'] ],
  [  'Result:  -->'  , 'result'   , ___ ,  ___        ,       _        ],
  [  HS('slider')    ,   ___      , ___ , '__value__' ,      Quit      ] )

while True:
    name, event = gui.get()

    if name == 'Calculate':
        try:
            gui.result = float(gui.num1) + float(gui.num2)
        except Exception as e:
            gui.result = 'Error: ' + str(e)

    # Original widget still accessible via widgets[]
    print(gui.widgets['result'].text())

    if name == 'slider':
        gui.value = gui.slider
    
    if name == 'value':
        gui.slider = gui.value

    elif name is None:
        break
