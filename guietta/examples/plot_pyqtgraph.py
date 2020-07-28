# -*- coding: utf-8 -*-


import numpy as np
from guietta import Gui, PG, PGI, III, VS, Exceptions

gui = Gui(
  [  PG('plot'),  VS('slider') ],
  [     III     ,  '^^^ Move the slider'  ],
  [ PGI('image') ,  '<< image'],
  exceptions =  Exceptions.OFF
    )

with gui.slider:
    t = np.linspace(0, 1+gui.slider/10, 400)
    gui.plot = np.tan(t)

    img = t.reshape((20,20))
    gui.image = img

gui.slider = 1

gui.run()
