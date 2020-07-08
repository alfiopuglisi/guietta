
Reference
=========

Layout
------

Guietta uses a grid layout (*QGridLayout*). Number of rows and columns
is automatically calculated from the input. There is typically one widget
per grid cell ( **_** will result in an empty cell), but widgets may span
multiple rows and/or columns as described below.

Syntax
++++++

To create a layout, instantiate a *guietta.Gui* object and pass it a series
of lists. Each list corresponds to a row of widgets. All lists must have
the same length.

As a special case, if a list contains a single widget, the widget will
be expanded to fill the whole row. This is useful for titles and
horizontal separators.

Widgets
-------

Here is the complete widget set::

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
      [  HS('slider2'),    ___         , ___                 ,      _       ] )
        
    gui.show()
  


+-----------------+---------------------------------------+-------------+
| Syntax          | Equivalent Qt widget                  | Event name  |
+=================+=======================================+=============+
| _               |   nothing (empty layout cell)         | none        |
+-----------------+---------------------------------------+-------------+
| | 'text'        |   QLabel('text')                      | 'text'      |
| | L('text')     |                                       |             |
+-----------------+---------------------------------------+-------------+
| | 'image.jpg'   |   QLabel with QPixmap('image.jpg')    | 'image'     |
| | L('image.jpg')|                                       |             |
+-----------------+---------------------------------------+-------------+
| | ['text']      |   QPushButton('text')                 | 'text'      |
| | B('text')     |                                       |             |
+-----------------+---------------------------------------+-------------+
| | ['image.jpg'] |   QPushButton(QIcon('image.jpg'), '') | 'image'     |
| | B('image.jpg')|                                       |             | 
+-----------------+---------------------------------------+-------------+
| '__name__'      |   QLineEdit(''), name set to 'name'   | 'name'      |
+-----------------+---------------------------------------+-------------+
| E('text')       |   QLineEdit('text')                   | 'text'      |
+-----------------+---------------------------------------+-------------+
| C('text')       |   QCheckBox('text')                   | 'text'      |
+-----------------+---------------------------------------+-------------+
| R('text')       |   QRadioButton('text')                | 'text'      |
+-----------------+---------------------------------------+-------------+
| P('name')       |   QProgressBar()                      | 'name'      |
+-----------------+---------------------------------------+-------------+
| HS('name')      |   QSlider(Qt::Horizontal)             | 'name'      |
+-----------------+---------------------------------------+-------------+
| VS('name')      |   QSlider(Qt::Horizontal)             | 'name'      |
+-----------------+---------------------------------------+-------------+
| HSeparator      |   Horizontal separator                |             |
+-----------------+---------------------------------------+-------------+
| VSeparator      |   Vertical separator                  |             |
+-----------------+---------------------------------------+-------------+
| M('name')       |   Matplotlib FigureCanvas*            |             |
+-----------------+---------------------------------------+-------------+
| PG('name')      |   pyqtgraph PlotWidget*               |             |
+-----------------+---------------------------------------+-------------+
| widget          |   any valid QT widget                 | none        |
+-----------------+---------------------------------------+-------------+
| (widget, 'name')|   any valid QT widget                 | 'name'      |
+-----------------+---------------------------------------+-------------+

* Matplotlib or pyqtraph will only be imported if the M() or PG() widgets
  are used. Matplotlib and pyqtgraph are not is not installed automatically
  together with guietta. If the M() widget  is used, the user must install
  matplotlib manually, same for PG() and pyqtgraph.

Buttons support both images and texts at the same time:

+----------------------------+-----------------------------+-------------+
| Syntax                     | Equivalent Qt widget        | Event name  |
+============================+=============================+=============+
| | ['image.jpg', 'text']    | QPushButton()               |  'text'     |
| | B('image.jpg', 'text')   | with image and text         |             |
+----------------------------+-----------------------------+-------------+



Continuations
-------------

How to extend widgets over multiple rows and/or columns::


    from guietta import Gui, HS, VS, _, ___, III
    
    gui = Gui(
    
       [ 'Big label', ___ , ___ , 'xxx' , VS('s1') ],
       [    III     , III , III , 'xxx' ,   III    ],
       [    III     , III , III , 'xxx' ,   III    ],
       [     _      ,  _  ,  _  , 'xxx' ,   III    ],
       [  HS('s2')  , ___ , ___ ,  ___  ,    _     ])


+--------------+----------------------------------------------------+
| Syntax       | Meaning                                            |
+==============+====================================================+
|    _         |   nothing (empty layout cell)                      |
+--------------+----------------------------------------------------+
|    ___       |   (three underscores) Horizontal widget span       |
+--------------+----------------------------------------------------+
|    III       |   (three capital letters i) vertical widget span   |
+--------------+----------------------------------------------------+

Rules:

 - all grid cells must contain either a widget, one of **___** or **III**,
   or **_**  if the cell is empty. Other values will cause a ValueError
   exception. Empty elements are not allowed by the Python list syntax
   and will cause a SyntaxError.
 - **___** can only be used to the right of a widget to extend it
 - **III** can only be used below a widget to extend it
 - **___** and **III** can be combined to form big rectangular widgets,
   with the widget to be extended in the top-left corner.

Signals
-------

Signals can be connected with gui.events() where each widget has:
    
+----------------------+-----------------------------------------------------+
| Syntax               | Meaning                                             |
+======================+=====================================================+    
|    _                 |  no connection                                      |
+----------------------+-----------------------------------------------------+
|    slot              | reference to Python callable, using the default     |
|                      | widget signal (if pre-defined, otherwise ValueError)|
+----------------------+-----------------------------------------------------+
| ('textEdited', slot) | tuple(signal name, Python callable)                 |
+----------------------+-----------------------------------------------------+

Table of default signals:

+----------------------+----------------------------------+
| Widget               | Signal                           |
+======================+==================================+    
|  QPushButton         |  clicked(bool)                   |
+----------------------+----------------------------------+
|  QLineEdit           |  returnPressed()                 |
+----------------------+----------------------------------+
|  QCheckBox           |  stateChanged(int)               |
+----------------------+----------------------------------+
|  QRadioButton        |  toggled())                      |
+----------------------+----------------------------------+
|  QAbstractSlider     |  valueChanged(int)               |
|  (QSlider, QDial,    |                                  |
|  QScrollBar)         |                                  |
|  QProgressBar        |                                  |
+----------------------+----------------------------------+
| QListWidget          |  currentTextChanged              |
+----------------------+----------------------------------+
| QComboBox            | textActivated                    |
+----------------------+----------------------------------+
                    
Widgets not listed in this table must be connected using the tuple syntax.

Properties
++++++++++

Table of properties created for each widget type:

+----------------------+--------------------+---------------------+
| Widget               | Read property type | Write property type |
+======================+====================+=====================+    
| QLabel,              |   str              | str                 |
| QLineEdit            |                    |                     | 
+----------------------+--------------------+---------------------+
| QAbstractButton      |                    |                     |
| (QPushButton,        |                    |                     |
| QCheckBox,           |                    |                     |
| QRadioButton)        |  widget instance   | callable            |
+----------------------+--------------------+---------------------+
| QAbstractSlider      |                    |                     |
| (QSlider, QDial,     |                    |                     |
| QScrollBar)          |  int               | int                 |
| QProgressBar         |                    |                     |
+----------------------+--------------------+---------------------+
| QAbstractItemView    |                    |                     |
| (QListWidget)        |  list of str       | list of str         |
+----------------------+--------------------+---------------------+
| QComboBox            |  dict{str: any}    | dict{str: any}      |
+----------------------+--------------------+---------------------+
| Everything else      |  widget instance   | raises an exception |
+----------------------+--------------------+---------------------+



Exception catching in slots
+++++++++++++++++++++++++++

When a slot is called, they will be enclosed in a "try - except Exception"
block. What happens in the except clause depends on the "exceptions"
keyword parameter of the GUI constructor, which accepts the following enums:

+---------------------------------+------------------------------------+
| Enum                            | Exception handling                 |
+=================================+====================================+    
|  Exceptions.OFF                 | nothing, exception is re-raised    |
+---------------------------------+------------------------------------+
|  Exceptions.POPUP (*default*)   | popup a QMessageBox.warning        |
|                                 | with the exception string          |
+---------------------------------+------------------------------------+
|  Exceptions.PRINT               | exception string printed on stdout |
+---------------------------------+------------------------------------+
|  Exceptions.SILENT              | nothing, exception is "swallowed"  |
+---------------------------------+------------------------------------+

