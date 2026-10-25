# guietta

A tool for making simple Python GUIs

Guietta is a tool that makes simple GUIs *simple*:

```python
from guietta import _, Gui, Quit
gui = Gui(
	[ "Enter numbers:",  "__a__", "+", "__b__", ["Calculate"] ],
	[    "Result: -->", "result",   _,       _,             _ ],
	[                _,        _,   _,       _,          Quit ]
)

with gui.Calculate:
	gui.result = float(gui.a) + float(gui.b)

gui.run()
```
And here it is:

![Example GUI](https://guietta.readthedocs.io/en/stable/_images/example.png)

Also featuring:
 * matplotlib and pyqtgraph integration, for easy event-driven plots
 * easily display columns of data in labels using lists and dicts
 * multiple windows
 * customizable behaviour in case of exceptions
 * queue-like mode (a la PySimpleGUI)
 * integrate any QT widget seamlessly, even your custom ones (as long as
   it derives from QWidget, it is OK)
 * easy background processing for long-running operations
 * ordinary QT signals/slots, accepting any Python callable, if you really
   want to use them

# Installation

Guietta works with any of the PySide6, PyQt6, PyQt5 and PySide2 Qt
bindings, through [QtPy](https://pypi.org/project/QtPy/). No binding is
installed automatically, so you can choose the one you prefer.
If you do not have one already, install guietta together with a binding:

    pip install guietta[pyside6]

(or `guietta[pyqt6]`, `guietta[pyqt5]`, `guietta[pyside2]`).
If a Qt binding is already installed, just use **pip install guietta**.

With conda:

    conda install -c conda-forge guietta

If more than one binding is installed, select one by setting the
`QT_API` environment variable to `pyside6`, `pyqt6`, `pyqt5` or `pyside2`.

If you use conda, please read our page on
[QT incompatibilities with conda](https://guietta.readthedocs.io/en/latest/qt_conda.html).

# Documentation

Stable version: https://guietta.readthedocs.io/en/stable/

Latest update from github: https://guietta.readthedocs.io/en/latest/

# Tests

[![Documentation Status](https://readthedocs.org/projects/guietta/badge/?version=stable)](https://guietta.readthedocs.io/en/stable/?badge=stable)
![](https://github.com/alfiopuglisi/guietta/workflows/pytest/badge.svg)
![](https://github.com/alfiopuglisi/guietta/workflows/lint_python/badge.svg)

