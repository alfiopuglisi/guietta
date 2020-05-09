# -*- coding: utf-8 -*-

from guietta import B, E, _, Gui, Quit

def do_eval(gui):
    try:
        gui.result = eval(gui.expr)
    except Exception as e:
        gui.result = 'Error: ' + str(e)


class Test(Gui):
    
    def __init__(self):
        super().__init__(        
    
  [  'Enter expression:', E('expr')   , B('Eval!') ],
  [  'Result:'          , 'result'    , _          ],
  [  _                  , _           , Quit       ] )

        self.events(

    [  _            , do_eval , do_eval ], 
    [  _            ,   _     , _       ], 
    [  _            ,   _     , _       ], )


gui = Test()
gui.run()

