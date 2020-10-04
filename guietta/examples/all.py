# -*- coding: utf-8 -*-

# Showcase of most available widgets, also demonstrating how
# to integrate other QT widgets directly in the layout.
#
# Written by Bill Wetzel and Alfio Puglisi.

from guietta import Gui, B, E, L, HS, VS, HSeparator, VSeparator
from guietta import Yes, No, Ok, Cancel, Quit, _, ___, III
from guietta import R1, R2, C, P

try:
    from PySide2.QtWidgets import QDial, QLCDNumber, QTableWidget
    from PySide2.QtWidgets import QTableWidgetItem, QHeaderView
except ImportError:
    from PyQt5.QtWidgets import QDial, QLCDNumber, QTableWidget
    from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView


gui = Gui(

  [ '<center>A big GUI with all of Guietta''s widgets</center>'],
  [ '<center>Move the dial!</center>'],
  [ HSeparator ],

  [ 'Label'    , 'imagelabel.jpeg' , L('another label')  , VS('slider1')],
  [  _         ,     ['button']    , B('another button') ,     III      ],
  [ '__edit__' ,  E('an edit box') , _                   ,   VSeparator ],
  [ R1('rad1') ,  R1('rad2')       , R1('rad3')          ,     III      ],
  [ R2('rad4') ,  R2('rad5')       , R2('rad6')          ,     III      ],
  [ C('ck1')   ,   C('ck2')        , C('ck3')            ,     III      ],
  [   Quit     ,        Ok         , Cancel              ,     III      ],
  [    Yes     ,        No         , _                   ,     III      ],
  [  HS('slider2'),    ___         , ___                 ,      _       ],
  [  (QDial, 'dial'),  (QLCDNumber, 'lcd')   , ___       ,      _       ],
  [  (QTableWidget, 'tab1'),  ___      , ___             ,      ___     ],
  [    III     , III , III , III ],
  [    III     , III , III , III ],
  [P('progbar'), (QLCDNumber, 'lcd2')   , _   ,  _    ],
  [   L('l1'),  L('l2'), L('l3'), L('l4')      ],
)

gui.window().setGeometry( 100, 100, 600, 900 )      # posx, posy, w, h

gui.widgets['dial'].setNotchesVisible( True )

gui.widgets['tab1'].setColumnCount( 4 )
gui.widgets['tab1'].setRowCount( 5 )
gui.widgets['tab1'].horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

gui.l1 = "Label 1"
gui.l2 = "This is Label 2"

for x in range( 4 ):
    for y in range( 5 ):
        item = QTableWidgetItem('%d %d' % (x, y))
        gui.widgets['tab1'].setItem( y, x, item )
        gui.widgets['tab1'].setHorizontalHeaderItem( x, QTableWidgetItem('Col: %d' % x ) )
        gui.widgets['tab1'].setVerticalHeaderItem( y, QTableWidgetItem('Row: %d' % y ) )

while True:
    name, event = gui.get()

    if name == 'slider1':
        gui.lcd.display( float(gui.slider1))
        gui.widgets['tab1'].itemAt( 0, 0 ).setText(str(gui.slider1))

    elif name == 'dial':
        gui.widgets['tab1'].itemAt( 0, 1 ).setText(str(gui.dial))
        gui.lcd2.display( float(gui.dial))
        gui.progbar = gui.dial

    elif name == None:
        break


