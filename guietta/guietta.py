# -*- coding: utf-8 -*-

import queue
import functools
from collections import Iterable

from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtWidgets import QPushButton, QRadioButton, QCheckBox
from PyQt5.QtWidgets import QLineEdit, QGridLayout, QSlider
from PyQt5.QtCore import Qt


if QApplication.instance() is None:
    app = QApplication([])


# Widget shortcuts

B = QPushButton
E = QLineEdit
C = QCheckBox
R = QRadioButton

def HS(name):  # Horizontal slider
    return X(QSlider(Qt.Horizontal), name)


def VS(name):  # Vertical slider
    return X(QSlider(Qt.Vertical), name)

class _:
    pass

class ___:   # Horizontal continuation
    pass

class I:     # Vertical continuation
    pass

class X:     # Generic unsupported widget
    def __init__(self, widget, name):
        self.widget = widget
        self.name = name

_specials = (_, ___, I)
_special_instances = (X,)

_default_signals = {QPushButton: 'clicked',
                    QLineEdit: 'returnPressed',
                    QCheckBox: 'stateChanged',
                    QSlider: 'valueChanged'}

# Standard buttons. We need to make a new instance every time one
# is requested, otherwise we risk cross-window connections.

class AutoConnectButton:
    def __init__(self, name):
        self._name = name

    def get(self, connect_to=None):
        button = QPushButton(self._name)
        if connect_to:
            button.clicked.connect(connect_to)
        return button


Quit = AutoConnectButton('Quit')
Ok = AutoConnectButton('Ok')
Cancel = AutoConnectButton('Cancel')
Yes = AutoConnectButton('Yes')
No = AutoConnectButton('No')


# Some helper functions


def _enumerate_lol(lol, skip_specials=True):
    for i, row in enumerate(lol):
        for j, element in enumerate(row):
            if skip_specials and element in _specials:
                continue
            yield i, j, element

def _iterable(x):
    return isinstance(x, Iterable) and not isinstance(x, str)

def _normalize(x):
    return ''.join(c for c in x if c.isalnum() or c == '_')

def _bound_method(method, to_whom):
    return hasattr(method, '__self__') and method.__self__ == to_whom

def _filter_lol(lol, func):
    for row in lol:
        for i in range(len(row)):
            row[i] = func(row[i])

def _auto_connect(slot, x):
    if isinstance(x, AutoConnectButton):
        x = x.get(connect_to=slot)
    return x

def _check_widget(x):
    if not isinstance(x, QWidget) and x not in _specials and not isinstance(x, X):
        raise ValueError('Element %s is not a widget' % x)
    return x

def _check_callable(x):
    if not callable(x) and x not in _specials:
        raise ValueError('Element %s is not callable' % x)
    return x

def _check_string(x):
    if not isinstance(x, str) and x not in _specials:
        raise ValueError('Element %s is not a string' % x)
    return x


def _layer_check(lol):
    '''
    Argument checking for layers.

    Checks that the arguments to a layer (__init__, events(), colors(), etc)
    are well-formed: a series of lists of equal lengths.
    and with valid elements. In case on any error, an exception
    will be raised.

    Parameters
    ----------
    *lists : any
        the arguments to check

    Raises
    ------
    ValueError
        In case the arugments are not lists or the lengths differ
    '''
    ncols = len(lol[0])
    for row in lol:
        if not _iterable(row):
            raise ValueError('Arguments are not lists (or iterables)')

        if len(row) != ncols:
            raise ValueError('Row lengths differ')

# Compact element processing

def _convert_compacts(x):

    if isinstance(x, str) and x.startswith('__') and x.endswith('__'):
        return QLineEdit(x[2:-2])

    elif isinstance(x, str):
        return QLabel(x)

    elif _iterable(x) and isinstance(x[0], str):
        return QPushButton(x[0])

    else:
        return x  # No change


class Gui:
    '''Main GUI object.

    The GUI is defined passing to the initializer a set of QT widgets
    organized in rows of equal length. All other method that expect
    lists (like events() or names()) will expect a series of list with
    the same length.

    Every widget will be added as an attribute to this instance,
    using the widget text as the attribute name (removing all special
    characters and only keeping letters, numbers and underscores.)
    '''

    def __init__(self, *lists):

        # Input argument checks
        _layer_check(lists)
        _filter_lol(lists, functools.partial(_auto_connect, self.close))
        _filter_lol(lists, _convert_compacts)
        _filter_lol(lists, _check_widget)

        self._layout = QGridLayout()
        self._widgets = {}    # widgets by name
        self._aliases = {}    # name aliases (1 alias per name)
        self._window = None

        self._get_handler = False   # These three for the get() method
        self._event_queue = queue.Queue()
        self._closed = False

        # Intermediate step that will be filled by replicating
        # widgets when ___ and I are encountered.
        step1 = [[None] * len(lists[0]) for i in range(len(lists))]

        for i, j, element in _enumerate_lol(lists, skip_specials=False):
            # Special cases. ___ and 'I' will replicate
            # the widgets from the previous column and row.
            if element == _:
                element = QLabel('')
            elif element == ___:
                step1[i][j] = step1[i][j-1]
                continue
            elif element == I:
                step1[i][j] = step1[i-1][j]
                continue

            step1[i][j] = element

        # Now a multi-cell widget has been replicated both in rows
        # and in columns. Look for repetitions to calculate spans.

        done = set()  # To avoid repeated insertions
        for i, j, element in _enumerate_lol(step1):
            if element not in done:
                rowspan = 0
                colspan = 0
                for ii in range(i, len(lists)):
                    if step1[ii][j] == element:
                        rowspan += 1
                for jj in range(j, len(lists[0])):
                    if step1[i][jj] == element:
                        colspan += 1

                widget, name = self._get_widget_and_name(element)
                self._layout.addWidget(widget, i, j, rowspan, colspan)
                self._widgets[name] = widget

                # Special case for QLineEdit, make it empty.
                if isinstance(element, QLineEdit):
                    element.setText('')

                done.add(element)

    def _get_widget_and_name(self, element):
        if isinstance(element, X):
            return element.widget, element.name

        name = None
        for methodname in ['text', 'currentText']:
            if hasattr(element, methodname):
                name = getattr(element, methodname).__call__()
                break
        else:
            raise ValueError('Unsupported widget. Please use X() instead.'
                             'Widget was: ' + str(element))

        name = _normalize(name)
        while name in self._widgets:
            name += '_'
        return element, name

    def events(self, *lists):
        '''Defines the GUI events

        The argument must be a layout with the same shape as the
        initializer. Every element is the callback function to be
        called when the default signal of the widget is fired.

        Bound methods are called without arguments. Functions and
        unbound methods will get a single argument with a reference
        to this Gui instance.
        '''
        # Input argument checks
        _layer_check(lists)
        _filter_lol(lists, _check_callable)

        for i, j, slot in _enumerate_lol(lists):
            item = self[i,j]
            try:
                signal = getattr(item, _default_signals[item.__class__])
            except KeyError as e:
                raise ValueError('Unsupported widget for events(): %s ' %
                                 str(item.__class__)) from e

            if _bound_method(slot, to_whom=self):
                signal.connect(slot)
            else:
                signal.connect(functools.partial(slot, self))

    def names(self, *lists):
        '''Overrides the default widget names

        The argument must be a layout with she same shape as the
        initializer. Every element is a string with a name alias
        for the widget in that position.
        '''
        _layer_check(lists)
        _filter_lol(lists, _check_string)

        names_by_widget = {v: k for k, v in self._widgets.items()}

        for i, j, alias in _enumerate_lol(lists):
            item = self[i,j]
            name = names_by_widget[item]
            self._aliases[alias] = name

    def colors(self, *args):
        '''Defines the GUI colors'''
        raise NotImplementedError

    def groups(self, *args):
        '''Defines the GUI widget groups'''
        raise NotImplementedError

    def __getattr__(self, name):
        '''Returns a widget using its name or alias'''

        if name in self._aliases:
            name = self._aliases[name]

        if name in self._widgets:
            return self._widgets[name]
        else:
            # Default behaviour
            raise AttributeError

    def __getitem__(self, name):
        '''Widget by coordinates [row,col]'''
        return self._layout.itemAtPosition(name[0], name[1]).widget()

    def all(group=''):
        '''Replicates command on all widgets'''
        raise NotImplementedError

    def layout(self):
        '''Returns the Gui layout, containing all the widgets'''
        return self._layout

    def window(self):
        '''Builds a QT window containin all the Gui widgets and returns it'''

        if self._window is None:
            self._window = QWidget()
            self._window.setLayout(self._layout)
        return self._window

    def import_into(self, obj):
        '''
        Widget importer

        Adds all this Gui's widget to `obj` as new attributes. Aliases
        defind with names() are also added.
        '''
        widgets = {**self._widgets, **self._aliases}

        for name, widget in widgets.items():
            if hasattr(obj, name):
                raise Exception('Cannot import: duplicate name %s ' % name)
            else:
                setattr(obj, name, widget)

    def run(self, argv=None):
        '''Display the Gui and start the event loop'''

        if argv is None:
            argv = []
        app = QApplication.instance()
        self.window().show()
        app.exec_()

    def close(self):
        if self._window:
            self._window.close()

    def get(self, block=True, timeout=None):
        '''Runs the GUI in queue mode

        In queue mode, no callbacks are used. Insted, the user should call
        gui.get() in a loop to get the events and process them.
        The QT event loop will stop in between calls to gui.get(), so
        event processing should be quick.

        get() will return (None, None) when the gui was closed.
        '''
        if self._closed:
            return (None, None)

        names_by_widget = {v: k for k, v in self._widgets.items()}

        if not self._get_handler:
            for widget in self._widgets.values():
                klass = widget.__class__
                if klass in _default_signals:
                    signal = getattr(widget, _default_signals[klass])
                    handler = functools.partial(self.event_handler,
                                                signal,
                                                widget)
                    signal.connect(handler)
            self._get_handler = True

        self._app = QApplication.instance()
        self.window().closeEvent = self.stop_handler
        self.window().show()
        self._closed = False
        self._app.exec_()  # Start event loop

        while True:
            try:
                signal, widget, *args = self._event_queue.get()
                if (signal, widget) == (None, None):
                    self._closed = True
                    return (None, None)
                return (names_by_widget[widget], signal.signal, *args)
            except queue.Empty:
                self._app.exec_()  # Restart event loop

    def event_handler(self, signal, widget, *args):
        self._event_queue.put((signal, widget, *args))
        self._app.exit()  # Stop event loop

    def stop_handler(self, event):
        self._event_queue.put((None, None))

# ___oOo___
