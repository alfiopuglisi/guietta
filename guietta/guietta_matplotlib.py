# -*- coding: utf-8 -*-

from matplotlib.figure import Figure
from matplotlib.colorbar import Colorbar
from matplotlib.backends.backend_qt5agg import FigureCanvas

from guietta import Signal, _alsoAcceptAnotherGui, Ax


class MatplotlibWidget(FigureCanvas):

    clicked = Signal(float, float)

    def __init__(self, width, height, dpi, subplots, animated=False, **kwargs):
        figure = Figure(figsize=(width, height), dpi=dpi)
        # DO not use add_subplots(), for compatibility with
        # old versions of maplotlib (<2.1)
        if subplots == (1,1):
            self.ax = figure.add_subplot(1,1,1)
        else:
            self.ax = []
            for x in range(subplots[0] * subplots[1]):
                self.ax.append(figure.add_subplot(subplots[0], subplots[1], x+1))
        self.kwargs = kwargs
        self.animated = animated
        self.plotobj = None
        super().__init__(figure)
        figure.canvas.mpl_connect('button_press_event',
                                  self._on_button_press)

    def _on_button_press(self, event):
        self.clicked.emit(event.xdata, event.ydata)

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
                errmsg = 'Matplotlib widgets need an array-like value'
                raise TypeError(errmsg) from e

            if len(arr.shape) not in [1,2]:
                raise ValueError('Value must be 1d or 2d, shape is %s instead' %
                                  str(arr.shape))
    
            if not self.animated or self.plotobj is None:
                with Ax(self) as ax:
                    if len(arr.shape) == 1:
                        self.plotobj = ax.plot(arr)
                    elif len(arr.shape) == 2:
                        self.plotobj = ax.imshow(arr)
            else:
                if len(arr.shape) == 1:
                    self.plotobj[0].set_ydata(arr)
                elif len(arr.shape) == 2:
                    self.plotobj.set_array(arr)
                self.ax.figure.canvas.draw()
            
        return (getx, setx)

# ___oOo___
