# -*- coding: utf-8 -*-

# Showcase of most available widgets, also demonstrating how
# to integrate other QT widgets directly in the layout.
#
# Written by Bill Wetzel and Alfio Puglisi.

from guietta import Gui, B, E, L, HS, VS, HSeparator, VSeparator
from guietta import Yes, No, Ok, Cancel, Quit, _, ___, III
from guietta import R, C

from PySide2.QtWidgets import QDial, QLCDNumber, QTableWidget, QProgressBar
from PySide2.QtWidgets import QTableWidgetItem, QHeaderView, QButtonGroup


gui = Gui(

  [ '<center>A big GUI with all of Guietta''s widgets</center>'],
  [ '<center>Move the dial!</center>'],
  [ HSeparator ],

  [ 'Label'    , 'imagelabel.jpeg' , L('another label')  , VS('slider1')],
  [  _         ,     ['button']    , B('another button') ,     III      ],
  [ '__edit__' ,  E('an edit box') , _                   ,   VSeparator ],
  [ R('rad1')  ,  R('rad2')        , R('rad3')           ,     III      ],
  [ R('rad4')  ,  R('rad5')        , R('rad6')           ,     III      ],
  [ C('ck1')   ,   C('ck2')        , C('ck3')            ,     III      ],
  [   Quit     ,        Ok         , Cancel              ,     III      ],
  [    Yes     ,        No         , _                   ,     III      ],
  [  HS('slider2'),    ___         , ___                 ,      _       ],
  [  (QDial, 'dial'),  (QLCDNumber, 'lcd')   , ___       ,      _       ],
  [  (QTableWidget, 'tab1'),  ___      , ___             ,      ___     ],
  [    III     , III , III , III ],
  [    III     , III , III , III ],
  [  (QProgressBar, 'progbar'),  (QLCDNumber, 'lcd2')   , _   ,  _    ],
  [   L('l1'),  L('l2'), L('l3'), L('l4')      ],
)

gui.window().setGeometry( 100, 100, 600, 900 )      # posx, posy, w, h

g1 = QButtonGroup()
g2 = QButtonGroup()
g1.addButton( gui.rad1 )
g1.addButton( gui.rad2 )
g1.addButton( gui.rad3 )
g2.addButton( gui.rad4 )
g2.addButton( gui.rad5 )
g2.addButton( gui.rad6 )

gui.widgets['dial'].setNotchesVisible( True )

gui.widgets['tab1'].setColumnCount( 4 )
gui.widgets['tab1'].setRowCount( 5 )
gui.widgets['tab1'].horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

gui.l1 = "Label 1"
gui.l2 = "This is Label 2"

for x in range( 4 ):
    for y in range( 5 ):
        item = QTableWidgetItem( f'{x}, {y}' )
        gui.widgets['tab1'].setItem( y, x, item )
        gui.widgets['tab1'].setHorizontalHeaderItem( x, QTableWidgetItem( f'Col: {x}' ) )
        gui.widgets['tab1'].setVerticalHeaderItem( y, QTableWidgetItem( f'Row: {y}' ) )

while True:
    name, event = gui.get()

    if name == 'slider1':
        gui.lcd.display( float(gui.slider1))
        gui.widgets['tab1'].itemAt( 0, 0 ).setText( f'{gui.slider1}' )

    elif name == 'dial':
        gui.widgets['tab1'].itemAt( 0, 1 ).setText( f'{gui.dial}' )
        gui.lcd2.display( float(gui.dial))
        gui.progbar.setValue( float(gui.dial))

    elif name == None:
        break


