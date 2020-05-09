# -*- coding: utf-8 -*-

from guietta import B, C, E, _, Gui, Quit

def do_eval(gui, *args):
    gui.result = eval(gui.expr)


def checkbox(gui, state):
    print('Checkbox state is', state)
    
gui = Gui(
    
  [  'Enter expression:', E('expr')  , B('Eval!') ],
  [  'Result:'          , 'result'    , _          ],
  [  C('test')          , _           , Quit       ] )


gui.events(
    
    [  _            ,   do_eval   , do_eval    ], 
    [  _            ,   _         , _          ], 
    [  checkbox     ,   _         , _          ], )


gui.run()

# GUI widgets are available after window closing,
print(gui.result)

    