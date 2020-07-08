# -*- coding: utf-8 -*-


import numpy as np
from guietta import Gui, PG, ___, III, _, VS

gui = Gui(
  [  PG('plot'),  ___, ___, VS('slider') ],
  [     III     , III, III,     III      ],
  [     III     , III, III,     III      ],
  [     III     , III, III,  '^^^ Move the slider'  ],
 )

with gui.slider:
    t = np.linspace(0, 1+gui.slider/10, 500)
    gui.plot.plot(t, np.tan(t), clear=True)

gui.slider = 1

gui.run()

    