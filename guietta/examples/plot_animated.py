# -*- coding: utf-8 -*-

import numpy as np
from guietta import Gui, ___, III, _, MA, VS

def replot(gui, value):
    t = np.linspace(0, 1+value/10, 500)
    gui.plot = np.tan(t)

def click(gui, x, y):
    print('Mouse click:', x, y)

gui = Gui(
    
  [  MA('plot'), ___, ___, VS('slider') ],
  [     III     , III, III,     III      ],
  [     III     , III, III,     III      ],
  [     III     , III, III,  '^^^ Move the slider'  ],
 )

gui.events(
    
    [  click        ,  _ , _ ,   replot    ], 
    [  _            ,  _ , _ ,   _          ], 
    [  _            ,  _ , _ ,   _          ], )


replot(gui, 1)

gui.run()

    
