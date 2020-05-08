# -*- coding: utf-8 -*-

from guietta import B, E, HS, _, Gui, Quit



gui = Gui(
    
  [  'Enter expression:', E('expr')  , B('Eval!') ],
  [  'Result:'          , 'result'    , _          ],
  [  HS('myslider')      , _        , Quit       ] )


while True:
    name, event = gui.get()

    if name == 'Eval':
        result = eval(gui.expr.text())
        gui.result.setText(str(result))
    
    if name == 'myslider':
        gui.result.setText(str(event.args[0]))

    elif name == None:
        break