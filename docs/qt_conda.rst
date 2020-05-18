
QT incompatibilities with conda
===============================

There have been reports of problems using PyQt5 in a conda environment,
for example:

 - https://github.com/ContinuumIO/anaconda-issues/issues/1970
 - https://github.com/ContinuumIO/anaconda-issues/issues/1554
 
It appears that the root cause is conda's renaming of "PyQt5" to "pyqt".
This leads pip to believe that PyQt5 is not installed, so it installs it,
resulting in two incompatible libraries and a crash at the first
"import PyQt5".

Guietta uses the `PySide2 Qt binding <https://pypi.org/project/PySide2/>`_,
so it should work around this problem, nevertheless we recommend caution
whe installing Guietta under conda. A good practice would be to make sure
that PySide2 is installed first:

 conda install PySide2
 
This way pip should detect it and avoid trying to install the pip version.