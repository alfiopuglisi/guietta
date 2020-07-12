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

![Example GUI](http://guietta.com/_images/example.png)

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

 **pip install guietta**

If you use conda, please read our page on
[QT incompatibilities with conda](https://guietta.readthedocs.io/en/latest/qt_conda.html).

## Install on older platforms


Guietta uses the [PySide2](https://pypi.org/project/PySide2/) QT binding
by default, and some systems
(older Macs, Raspberry PI) do not have it available. Guietta can fallback
to the PyQt5 binding if available, but does not specify it as an automatic
dependency. If you get an
installation error about PySide2, try to use PyQt5 instead using the
following:

```
    pip install guietta --no-deps
    pip install pyqt5
```

# Documentation

Stable version: https://guietta.readthedocs.io/en/stable/

Latest update from github: https://guietta.readthedocs.io/en/latest/

# Tests

[![Documentation Status](https://readthedocs.org/projects/guietta/badge/?version=stable)](https://guietta.readthedocs.io/en/stable/?badge=stable)
![](https://github.com/alfiopuglisi/guietta/workflows/pytest/badge.svg)
![](https://github.com/alfiopuglisi/guietta/workflows/lint_python/badge.svg)

