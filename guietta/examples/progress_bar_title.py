# -*- coding: utf-8 -*-

from guietta import Gui, P, Empty


gui = Gui(
    
  [  'Percent completed:', P('progress') ],
  
  title = 'ProgressBar test'

)

for counter in range(100):
    try:
        name, event = gui.get(timeout=0.1)
    except Empty:
        pass

    gui.progress = counter
