
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


Also featuring:
 - matplotlib and pyqtgraph integration, for easy event-driven plots
 - easily display columns of data in labels using lists and dicts
 - multiple windows
 - customizable behaviour in case of exceptions
 - queue-like mode (a la PySimpleGUI)
 - integrate any QT widget seamlessly, even your custom ones (as long as
   it derives from QWidget, it is OK)
 - easy background processing for long-running operations
 - ordinary QT signals/slots, accepting any Python callable, if you really
   want to use them
 
Installation
============

Using Conda
+++++++++++

Guietta is available on the conda-forge community channel:

 **conda install -c conda-forge guietta**

*Warning*: if you are managing your environments with Conda, do not use the
pip installer. Guietta installs fine either way, but one of its
dependences (PySide2) will break things (`details <qt_conda.html>`_).

Using Pip
+++++++++

 **pip install guietta**

 
Install on older platforms
++++++++++++++++++++++++++

Guietta uses the `PySide2 <https://pypi.org/project/PySide2/>`_ QT5 binding
by default, and some systems
(older Macs, Raspberry PI) do not have it available. Guietta can fallback
to the PyQt5 binding if available, but does not specify it as an automatic
dependency. If you get an
installation error about PySide2, try to use PyQt5 instead using the
following::

    pip install guietta --no-deps
    pip install pyqt5

Screenshots
===========

.. image:: guietta_screenshot_psd.png
    :width: 300px

Guietta at work in a scientific lab, showing an interactive plot.

Tutorial
========

Direct link to the tutorial: `tutorial.html <tutorial.html>`_.

See also the rest of the `documentation <index.html#id1>`_ below.


Source code
===========

https://github.com/alfiopuglisi/guietta


Troubleshooting
===============

Guietta uses Qt5, and some Linux distributions, like Ubuntu 16.04, appear
to have an incomplete default installation. If you encounter trouble
running guietta, please read the
`troubleshooting guide <troubleshooting.html>`_.


Documentation
=============

.. toctree::
   :maxdepth: 1

   intro
   tutorial
   reference
   internals
   changelog_link

