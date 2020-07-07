# -*- coding: utf-8 -*-

from guietta import Gui, _, ___, III, HValueSlider, VValueSlider, Qt

def do_slider(gui, value):
    print('Slider value: ', value)
    
slider1 = HValueSlider('hvalue', range(500), unit='Hz')    
slider2 = HValueSlider('hvalue', range(500), unit='Hz', anchor=Qt.AnchorLeft) 
slider3 = VValueSlider('hvalue', range(500))    

gui = Gui(
    
  [  'xxx' , ['xxx'], 'xxx' , slider3],
  [  slider1,   ___   , ___ ,   III  ],
  [  slider2,   ___   ,  _  ,   III  ],
  )


gui.events(
    
  [     _     ,    _    ,   _  ,  _  ],
  [  do_slider,    _    ,   _  ,  _  ],
  [     _     ,    _    ,   _  ,  _  ],
   )


gui.run()

    