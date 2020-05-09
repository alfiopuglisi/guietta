# -*- coding: utf-8 -*-

from guietta import B, E, _, Gui, Quit

def do_eval(gui):
    try:
        gui.result = eval(gui.expr)
    except Exception as e:
        gui.result = 'Error: ' + str(e)

gui = Gui(
    
  [  'Enter expression:', E('expr')  , B('Eval!') ],
  [  'Result:'          , 'result'    , _          ],
  [  _                  , _           , Quit       ] )


gui.events(
    
    [  _            ,   do_eval   , do_eval    ], 
    [  _            ,   _         , _          ], 
    [  _            ,   _         , _          ], )


gui.run()

# GUI widgets are available after window closing,
print(gui.result)

    