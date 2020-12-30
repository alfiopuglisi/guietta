
QT incompatibilities with conda
===============================

Guietta is available on both pip and conda (on the conda-forge channel).
In both cases, several dependencies will be installed too. Unfortunately,
one of those dependencies (`PySide2 <https://pypi.org/project/PySide2/>`_)
can wreak havoc on conda environments when installed from pip.

PySide2 is the official Python binding for Qt5. Another third-party
binding exists, with the official-sounding name of PyQt5. The conda
package for the latter has been renamed "pyqt".

This renaming leads pip to believe that PyQt5 is not installed,
so it installs it, resulting in two incompatible libraries and a crash
at the first "import PyQt5".

For reasons that I (the Guietta author) do not fully understand,
this also affects the PySide2 binding.

If for some reason you installed guietta with conda and PySide2 with pip,
and find that your conda environments do not work anymore, you can
try to fix the situation by forcing an install of PySide2 with conda:

  conda install -c conda-forge pyside2


Some bug reports about the problems of Conda with Qt5:

- https://github.com/ContinuumIO/anaconda-issues/issues/1970
- https://github.com/ContinuumIO/anaconda-issues/issues/1554
 
