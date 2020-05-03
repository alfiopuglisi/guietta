# -*- coding: utf-8 -*-

'''
A simple GUI which evaluates Python expressions
and displays the result.
Communication with the background task is asynchronous
thanks to a QueueListener that sends custom signals

'''

import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QLineEdit, QHBoxLayout, QVBoxLayout

from quickgui.framework import QuickQtGui, handler

# g is a reference to guietta, but we avoid a second import.
from guietta import B, E, _, Gui


    
class MotorGui(QuickQtGui):

    def __init__(self, qin, qout):
        super().__init__(qin, qout)

        gui = Gui(
            
          [  _('Simulation'), B('On')    , B('Off'), _('sim_status') ],
          [  _('Position'),   _('curpos'), _       , _('moving')     ], 
          [  _('Move to:'),   E('usrpos'), _       , B('Move')       ] )
         
        gui.events(

          [  _            , self.sim_on  , self.sim_off  ,       ],
          [  _            ,   _          , _             ,       ], 
          [  _            , self.move    , _             , self.move  ] )

        # layout() is mandatory, the rest is optional
        # Possible additional layers:
            # colors, fonts
            # names, overriding the default one
            # grouping (for things like g.disable() or g.all())
        
        # Widgets are automatically named from their label, unless 
        # overriden in the names layer, and added to module scope.
        # Whitespace and special characters are just removed.
        gui.Moveto.setText('foo')
        
        # Name clashes with method functions are handled automatically
        # because if you call something, it's a module function, while
        # if you dereference it with "." it's a widget.

        # Widget shortcuts
        # B=Button(), _=Label, E=Lineedit, C=Checkbox, R=Radio, S=slider,
        # Any QT class can be used directly if wanted instead of the shortcuts

        # Radio are exclusive across the whole window by default. If you
        # want different groups, use the groups layer.

        # All widgets are normal QT widgets so they support all QT methods.
        gui.Position.setColor(g.red)

        # Additional signal/slot connection        
        gui.usrpos.returnPressed.connect(another_method)

        # It's possible to go by coordinates [row, col]
        gui[0,1].setFont('Courier')

        # Replicate a call to all widgets, or just to a group
        gui.all(group='').disable()

        # Invalid references cause an exception
        gui.pippo.setText('ciao')

        # All-in-one application and event loop, but intermediate steps
        # are available
        gui.run(sys.argv)


    def move(self):
        self.send('MOVE ' + g.usrpos.text())

    def sim_on(self):
        self.send('SIMUL 1')

    def sim_off(self):
        self.send('SIMUL 0')

    @handler('MOVING')
    def refresh_status(self, data):
        moving = 'MOVING' if int(data) else 'IDLE'
        g.curstatus.setText(moving)

    @handler('POS')
    def refresh_pos(self, data):
        g.curpos.setText(data)

    @handler('SIMULATED')
    def refresh_simul(self, data):
        simul = 'On' if int(data) else 'Off'
        g.sim_status.setText(simul)

# ___oOo___
