# -*- coding: utf-8 -*-
'''
List of widget shortcuts:
    
    'text'         ->   QLabel('text')
    'image.jpg'    ->   QLabel with QPixmap('image.jpg'), name set to 'image'
    L('text')      ->   same as 'text'
    L('image.jpg') ->   same as 'image.jpg'
    ['text']       ->   QPushButton('text')
    ['image.jpg']  ->   QPushButton(QIcon('image.jpg')), name set to 'image'
    B('text')      ->   same as ['text']
    B('image.jpg') ->   same as ['image.jpg']
    '__name__'     ->   QLineEdit(''), name set to 'name'
    E('text')      ->   QLineEdit('text')
    C('text')      ->   QCheckBox('text')
    R('text')      ->   QRadioButton('text')
    HS('name')     ->   QSlider(Qt::Horizontal), name set to 'name'
    VS('name')     ->   QSlider(Qt::Horizontal), name set to 'name'
    widget         ->   any valid QT widget is accepted
    X(widget, name)->   any valid QT widget, name set to 'name'
    _              ->   QLabel('')
    ___            ->   (three underscores) Horizontal widget span
    III            ->   (three capital letters i) vertical widget span
'''

import queue
import os.path
import functools
import itertools
from collections import Iterable

from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtWidgets import QPushButton, QRadioButton, QCheckBox
from PyQt5.QtWidgets import QLineEdit, QGridLayout, QSlider
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QTimer


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

class III:
    pass

class _:
    pass

class ___:   # Horizontal continuation
    pass

global_images_dir = os.curdir
global_aliases = {}

def L(text_or_filename):     # Vertical continuation or image
    if not os.path.isabs(text_or_filename):
        fullpath = os.path.join(global_images_dir, text_or_filename)

    if os.path.exists(fullpath):
        label = QLabel()
        label.setPixmap(QPixmap(fullpath))
    else:
        label = QLabel(text_or_filename)
    return label

def B(text_or_filename, name=''):
    if not os.path.isabs(text_or_filename):
        fullpath = os.path.join(global_images_dir, text_or_filename)

    if os.path.exists(fullpath):
        button = QPushButton(QIcon(fullpath), name)
        if name == '':
            name, _ = os.path.splitext(text_or_filename)
            global_aliases[button] = name
            return button
    else:
        return QPushButton(text_or_filename)

class X:     # Generic unsupported widget
    def __init__(self, widget, name):
        self.widget = widget
        self.name = name

_specials = (_, ___, III)
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

class Empty(Exception):
    pass

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
        return L(x)   # Use L instead of QLabel to get automatic images

    elif _iterable(x) and isinstance(x[0], str):
        return B(x[0])  # Use B instead of QPushButton to get automatic images

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
        self._inverted = False

        # Intermediate step that will be filled by replicating
        # widgets when ___ and I are encountered.
        step1 = [[None] * len(lists[0]) for i in range(len(lists))]

        for i, j, element in _enumerate_lol(lists, skip_specials=False):
            # Special cases. ___ and 'I' will replicate
            # the widgets from the previous column and row.
            if element == _:
                element = None
            else:
                if element == ___:
                    if j > 0:
                        element = step1[i][j-1]
                    else:
                        raise IndexError('___ at the beginning of a row')
                if element == III:
                    if i > 0:
                        element = step1[i-1][j]
                    else:
                        raise IndexError('III at the start of a column')
                if element == None:
                    raise ValueError('Continuation from empty slot')

            step1[i][j] = element

        # Now a multi-cell widget has been replicated both in rows
        # and in columns. Look for repetitions to calculate spans.

        done = set([None])  # Skip empty elements
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

    @staticmethod
    def set_images_dir(images_dir):
        global global_images_dir
        global_images_dir = images_dir

    def _get_widget_and_name(self, element):
        if isinstance(element, X):
            return element.widget, element.name

        if element in global_aliases:
            name = global_aliases[element]
        else:
            if hasattr(element, 'text'):
                name = element.text()
            else:
                name = element.__class__.__name__

        name = _normalize(name)

        # If the name is a duplicate, auto-number it starting with 2.
        if name in self._widgets:
            for n in itertools.count(start=2):
                new_name = name + str(n)
                if new_name not in self._widgets:
                    name = new_name
                    break

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

    def _invert_dicts(self):
        if not self._inverted:
            self._names_by_widget = {v: k for k, v in self._widgets.items()}
            self._alias_by_name = {v: k for k, v in self._aliases.items()}
            self._inverted = True

    def _widget_name_or_alias(self, widget):
        '''Returns the alias or, failing that, the name for the widget'''
        name = self._names_by_widget[widget]
        if name in self._alias_by_name:
            return self._alias_by_name[name]
        else:
            return name

    def get(self, block=True, timeout=None):
        '''Runs the GUI in queue mode

        In queue mode, no callbacks are used. Insted, the user should call
        gui.get() in a loop to get the events and process them.
        The QT event loop will stop in between calls to gui.get(), so
        event processing should be quick.

        Every time an event happens, get() will return a variable length tuple:

            name, signal, *args = gui.get()

        where `name` is widget name that generated the event, signal is the
        PyQT signal description (a string), and args is a list with the
        signal arguments. At least one argument is guaranteed. For signals
        that have no arguments, args will be [False].

        get() will return (None, None, None) after the gui is closed.
        '''
        if self._closed:
            return (None, None, None)

        self._invert_dicts()

        # Connect handler for all events
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

        if (block is False) or (timeout is not None):
            if (block is False) or (timeout < 0):
                timeout = 0
            QTimer.singleShot(timeout * 1000,
                              Qt.PreciseTimer,
                              self.timeout_handler)

        self._app.exec_()  # Start event loop. Handler will stop it

        signal, widget, *args = self._event_queue.get()
        if signal == 'timeout':
            raise Empty
        elif signal is None:
            self._closed = True
            return (None, None, None)
        else:
            name = self._widget_name_or_alias(widget)
            return (name, signal.signal, *args)

    def event_handler(self, signal, widget, *args):
        self._event_queue.put((signal, widget, *args))
        self._app.exit()  # Stop event loop

    def stop_handler(self, event):
        self._event_queue.put((None, None, None))
        self._app.exit()  # Stop event loop

    def timeout_handler(self):
        self._event_queue.put(('timeout', None, None))
        self._app.exit()  # Stop event loop

# ___oOo___
