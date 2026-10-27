# -*- coding: utf-8 -*-

from guietta import _alsoAcceptAnotherGui

import numpy as np
import pyqtgraph


def _version_tuple(version):
    '''Numeric tuple from a version string, e.g. "0.11.0rc1" -> (0, 11, 0)'''
    return tuple(int(''.join(c for c in x if c.isdigit()) or 0)
                 for x in version.split('.'))


if _version_tuple(pyqtgraph.__version__) < (0, 11, 0):
    raise Exception('Minimum version for pyqtgraph is 0.11.0,'
                    'you have '+pyqtgraph.__version__)


def _to_array(x):
    try:
        return np.array(x)
    except Exception as e:
        errmsg = 'pyqtgraph widgets need an array-like value'
        raise TypeError(errmsg) from e


class _PyQtGraphMixIn:
    '''Common guietta property for pyqtgraph widgets.

    Derived classes must define _ndims (the accepted array dimensions)
    and _display(arr).
    '''

    def __init__(self, **kwargs):
        super().__init__()
        self.kwargs = kwargs

    def __guietta_property__(self):

        def getx():
            return self

        @_alsoAcceptAnotherGui(self)
        def setx(x):
            if x is None:
                return

            arr = _to_array(x)
            if arr.ndim not in self._ndims:
                raise ValueError('Value must be %s, shape is %s instead'
                                 % (' or '.join('%dd' % n for n in self._ndims),
                                    str(arr.shape)))
            self._display(arr)

        return (getx, setx)

    def _apply_kwargs(self):
        for k, v in self.kwargs.items():
            getattr(self, k)(v)


class PyQtGraphPlotWidget(_PyQtGraphMixIn, pyqtgraph.PlotWidget):

    _ndims = (1,)

    def _display(self, arr):
        self.plot(arr, clear=True)
        self._apply_kwargs()


class PyQtGraphImageView(_PyQtGraphMixIn, pyqtgraph.ImageView):
    '''Property for pyqtgraph image widgets'''

    _ndims = (2, 3)

    def _display(self, arr):
        self.setImage(arr)
        self._apply_kwargs()
        self.getHistogramWidget().hide()

# ___oOo___
