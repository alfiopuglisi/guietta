
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
        gui.result = float(gui.a) + float(gui.b)
    
    gui.run()


And here it is:

.. image:: example.png

More complicated examples are shown here:

`More screenshots <more_screenshots.html>`_.

Installation
============

 **pip install guietta**


Source code
===========

https://github.com/alfiopuglisi/guietta

Troubleshooting
===============

Guietta uses Qt5, and some Linux distributions, like Ubuntu 16.04, appear
to have an incomplete default installation. If you encounter trouble
running guietta, please read the
`troubleshooting guide <troubleshooting.html>`_.

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

