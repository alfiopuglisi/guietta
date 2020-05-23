# -*- coding: utf-8 -*-

from guietta import Gui, B, E, L, HS, VS, HSeparator, VSeparator
from guietta import Yes, No, Ok, Cancel, Quit, _, ___, III

gui = Gui(

   [ '<center>A big GUI with all of Guietta''s widgets</center>'],
   [ HSeparator ],

  [ 'Label'    , 'imagelabel.jpeg' , L('another label')  , VS('slider1')],
  [  _         ,     ['button']    , B('another button') ,     III      ],
  [ '__edit__' ,  E('an edit box') , _                   ,   VSeparator ],
  [   Quit     ,        Ok         , Cancel              ,     III      ],
  [    Yes     ,        No         , _                   ,     III      ],
   [ HSeparator ],
  [  HS('slider2'),    ___         , ___                 ,      _       ])
    
dummy = gui.get()
