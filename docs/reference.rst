
Reference
=========

Layout
------

Guietta uses a grid layout (*QGridLayout*). Number of rows and columns
is automatically calculated from the input. There is typically one widget
per grid cel (or *_* if the cell is empty), but widgets may span multiple
rows and/or columns as described below.

Syntax
++++++

To create a layout, instantiate a *guietta.Gui* object and pass it a series
of list. Each list correspond to a row of widgets. All lists must have
the same length.

Widgets
-------

Here is the complete widget set::

    from guietta import Gui, B, E, L, HS, VS
    from guietta import Yes, No, Ok, Cancel, Quit, _, ___, III
    
    gui = Gui(
    
       [ 'A big GUI with all of Guietta''s widgets', ___, ___, ___],
    
      [ 'Label'    , 'imagelabel.jpeg' , L('another label')  , VS('slider1')],
      [ 'button 1' ,    ['button 2']   , B('another Button') ,     III      ],
      [ '__edit__' ,  E('an edit box') , _                   ,     III      ],
      [   Quit     ,        Ok         , Cancel              ,     III      ],
      [    Yes     ,        No         , _                   ,     III      ],
      [  HS('slider2'),    ___         , ___                 ,      _       ])
  


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
| HS('name')      |   QSlider(Qt::Horizontal)             | 'name'      |
+-----------------+---------------------------------------+-------------+
| VS('name')      |   QSlider(Qt::Horizontal)             | 'name'      |
+-----------------+---------------------------------------+-------------+
| Separator       |   Horizontal separator                |             |
+-----------------+---------------------------------------+-------------+
| VSeparator      |   Vertical separator                  |             |
+-----------------+---------------------------------------+-------------+
| widget          |   any valid QT widget is accepted     | none        |
+-----------------+---------------------------------------+-------------+
| (widget, 'name')|   any valid QT widget is accepted     | 'name'      |
+-----------------+---------------------------------------+-------------+

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

 - **_**  can appear anywhere
 - **___** can only be used to the right of a widget to extend it
 - **III** can only be used below a widget to extend it
 - **___** and **III** can be combined to form big rectangular widgets,
   with the widget to be extended in the top-left corner.

Signals
-------

Signals can be connected with gui.events() where every widget has:
    
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





