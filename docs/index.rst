
Guietta!
========

Guietta is a tool that makes simple GUIs *simple*::


    from guietta import _, Gui, Quit
    
    gui = Gui(
        
      [  'Enter numbers:', '__a__'  , '+' , '__b__',  ['Calculate'] ],
      [  'Result:  -->'  , 'result' ,  _  ,    _   ,       _        ],
      [  _               ,    _     ,  _  ,    _   ,      Quit      ]
    )

    with gui.Calculate:
        gui.result = float(gui.num1) + float(gui.num2)
    
    gui.run()


And here it is:

.. image:: example.png


Installation
============

 **pip install guietta**
 

If you use conda, please read our page on
`QT incompatibilities with conda <qt_conda.html>`_.

Documentation
=============

.. toctree::
   :maxdepth: 1

   intro
   tutorial
   reference
   internals

