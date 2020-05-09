# -*- coding: utf-8 -*-

from guietta import _, Gui, Quit

# Compact definitions:
# Labels are just strings (now standard)
# A button is a string between square parenthesis (a 1-element sequence)
# an edit box is a string with double underscores

gui = Gui(
    
  [  'Enter expression:', '__expr__'   , ['Eval!'] ],
  [  'Result:'          , 'result'    , _          ],
  [  _                  , _           , Quit       ] )

gui.run()

print('Result: ', gui.result)