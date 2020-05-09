# -*- coding: utf-8 -*-

from guietta import B, E, _, Gui, Quit

class Test(Gui):
    
    def __init__(self):
        super().__init__(        
    
  [  'Enter expression:', E('expr')   , B('Eval!') ],
  [  'Result:'          , 'result'    , _          ],
  [  _                  , _           , Quit       ] )

        self.events(

    [  _            , self.do_eval, self.do_eval ], 
    [  _            ,   _         , _            ], 
    [  _            ,   _         , _            ], )

    def do_eval(self):
        try:
            self.result = eval(self.expr)
        except Exception as e:
            self.result = 'Error: ' + str(e)


gui = Test()
gui.run()

