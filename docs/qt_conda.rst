QT incompatibilities with conda
===============================

Guietta is available on both pip and conda (on the conda-forge channel).
Mixing the two installers for the Qt bindings can wreak havoc on conda
environments.

Conda and pip use different package names for the same Qt bindings:
for example, the PyQt5 binding is called "PyQt5" on pip, but "pyqt"
on conda. If a package installed with pip requires "PyQt5", pip may not
recognize the conda version, and installs a second copy, resulting
in two incompatible Qt libraries and a crash at the first import.

For this reason, guietta does not require any specific
Qt binding. It uses `QtPy <https://pypi.org/project/QtPy/>`_ to work with
whichever binding is already installed (PySide6, PyQt6, PyQt5 or PySide2).

In a conda environment, install both guietta and the Qt binding with conda::

  conda install -c conda-forge guietta pyside6

If guietta must be installed with pip in a conda environment, install
the binding with conda first, and then guietta with pip *without* any extra::

  conda install -c conda-forge pyside6
  pip install guietta

If your conda environment is already broken because of a binding installed
with pip, uninstall the pip copy (e.g. ``pip uninstall PySide2``) and
reinstall the binding with conda.

Some bug reports about the problems of Conda with Qt5:

- https://github.com/ContinuumIO/anaconda-issues/issues/1970
- https://github.com/ContinuumIO/anaconda-issues/issues/1554
