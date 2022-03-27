# -*- coding: utf-8 -*-

import numpy as np
from guietta import Gui, ___, III, _, MA, VS

def replot(gui, value):
    img = np.random.randn(100,100)
    gui.plot = img
    print('replot')

def click(gui, x, y):
    print('Mouse click:', x, y)

gui = Gui(
    
  [  MA('plot'), ___, ___, VS('slider') ],
  [     III     , III, III,  '^^^ Move the slider'  ],
 )

gui.events(
    
    [  click        ,  _ , _ ,   replot    ], 
)

replot(gui, 1)

gui.run()

    
