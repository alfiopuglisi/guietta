# -*- coding: utf-8 -*-

from guietta import _alsoAcceptAnotherGui

import pyqtgraph

if pyqtgraph.__version__ < '0.11.0':
    raise Exception('Minimum version for pyqtgraph is 0.11.0,'
                    'you have '+pyqtgraph.__version__)


class PyQtGraphPlotWidget(pyqtgraph.PlotWidget):
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
    
            import numpy as np
            try:
                arr = np.array(x)
            except Exception as e:
                errmsg = 'pyqtgraph widgets need an array-like value'
                raise TypeError(errmsg) from e
    
            if len(arr.shape) == 1:
                self.plot(arr, clear=True)
                for k,v in self.kwargs.items():
                    getattr(self, k).__call__(v)
            else:
                raise ValueError('Value must be 1d, shape is %s instead'
                                 % str(arr.shape))
    
        return (getx, setx)


class PyQtGraphImageView(pyqtgraph.ImageView):
    def __init__(self, **kwargs):
        super().__init__()
        self.kwargs = kwargs

    def __guietta_property__(self):
        '''Property for pyqtgraph image widgets'''
    
        def getx():
            return self
    
        @_alsoAcceptAnotherGui(self)
        def setx(x):
            if x is None:
                return
    
            import numpy as np
            try:
                arr = np.array(x)
            except Exception as e:
                errmsg = 'pyqtgraph widgets need an array-like value'
                raise TypeError(errmsg) from e
    
            if len(arr.shape) == 2:
                self.setImage(arr)
                for k,v in self.kwargs.items():
                    getattr(self, k).__call__(v)
                self.getHistogramWidget().hide()
            else:
                raise ValueError('Value must be 2d, shape is %s instead'
                                 % str(arr.shape))
        return (getx, setx)

# ___oOo___
