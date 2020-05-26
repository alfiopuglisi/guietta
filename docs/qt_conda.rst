
QT incompatibilities with conda
===============================

Short version: before or after installing guietta, also install PySide2
using conda::


  conda install -c conda-forge pyside2

This command sometimes takes a lot of time to complete. Give it time.

Long version:

pip and conda do not work well together. In particular, Conda ships
with a default QT library, which is not detected by pip. When guietta
is installed, pip will automatically install its version of PySide2
as a dependency. Unfortunately the two libraries are not binary compatible,
and this will lead to a crash when PySide2 is imported.

This is fixed by installing PySide2 with conda, before or after guietta
is installed, using this command::

  conda install -c conda-forge pyside2

A new conda-compatible copy  of PySide2 will be installed, that
should work without problems.

Some bug reports about the problems of Conda with Qt5:

- https://github.com/ContinuumIO/anaconda-issues/issues/1970
- https://github.com/ContinuumIO/anaconda-issues/issues/1554
 
It appears that the root cause is conda's renaming of "PyQt5" to "pyqt".
This leads pip to believe that PyQt5 is not installed, so it installs it,
resulting in two incompatible libraries and a crash at the first
"import PyQt5".

Guietta uses the `PySide2 Qt binding <https://pypi.org/project/PySide2/>`_,
but it seems to suffer from the same problem.
