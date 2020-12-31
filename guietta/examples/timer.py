# -*- coding: utf-8 -*-

from guietta import Gui, Quit, _

counter=0
def regular_update(gui):
    global counter
    counter += 1
    gui.counter = counter

def myeval(gui):
    gui.result = eval(gui.expr)

def reset(gui):
    global counter
    counter=0

def stop(gui):
    gui.timer_stop()

def start(gui):
    gui.timer_start(regular_update, interval=0.1)


gui = Gui(
    
  [  'Enter expression:', '__expr__'  , ['Eval!'] ],
  [  'Result:'          , 'result'    , _         ],
  [  ['Start']          , ['Stop']    , ['Reset'] ],
  [  'counter'          , _           , Quit      ] )

gui.events(
    
  [        _            ,    myeval   ,   myeval   ],
  [        _            ,    _        ,    _       ],
  [     start           ,   stop      ,   reset    ],
  [        _            ,    _        ,    _       ],  )

start(gui)
gui.run()


    

