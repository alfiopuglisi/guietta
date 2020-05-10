# -*- coding: utf-8 -*-

import numpy as np
from guietta import Gui, ___, III, _, M, Ax, VS

def replot(gui, value):

    with Ax(gui.plot) as ax:
        ax.set_title('y=tan(x)')
        t = np.linspace(0, 1+value/10, 500)
        ax.plot(t, np.tan(t), ".-")
 

gui = Gui(
    
  [  M('plot'), ___, ___, VS('slider') ],
  [     III     , III, III,     III      ],
  [     III     , III, III,     III      ],
  [     III     , III, III,  '^^^ Move the slider'  ],
 )

gui.events(
    
    [  _            ,  _ , _ ,   replot    ], 
    [  _            ,  _ , _ ,   _          ], 
    [  _            ,  _ , _ ,   _          ], )

replot(gui, 1)

gui.run()

    