# -*- coding: utf-8 -*-

from guietta import B, E, _, Gui, Quit

# Use *args to accept multiple signals
# with different arugments.
def do_eval(gui, *args):
    gui.result = eval(gui.expr)


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

    