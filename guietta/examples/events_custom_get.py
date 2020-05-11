# -*- coding: utf-8 -*-

from guietta import E, _, Gui, Quit

gui = Gui(
    
  [  'Enter expression:', E('expr')  , _ ],
  [  'Result:'          , 'result'    , _          ],
  [  _                  , _           , Quit       ] )


gui.events(
    
    [  _            ,   ('textEdited', None) , _    ], 
    [  _            ,   _                       , _    ], 
    [  _            ,   _                       , _    ], )


while True:
    name, event = gui.get()

    if name == 'expr':
        try:
            gui.result = eval(gui.expr)
        except Exception as e:
            gui.result = 'Error: ' + str(e)

    elif name == None:
        break
    