# -*- coding: utf-8 -*-
'''
List of widget shortcuts:

    'text'         ->   QLabel('text')
    'image.jpg'    ->   QLabel with QPixmap('image.jpg'), name is 'image'
    L('text')      ->   same as 'text'
    L('image.jpg') ->   same as 'image.jpg'
    ['text']       ->   QPushButton('text')
    ['image.jpg']  ->   QPushButton(QIcon('image.jpg'), ''), name is 'image'
    B('text')      ->   same as ['text']
    B('image.jpg') ->   same as ['image.jpg']
    '__name__'     ->   QLineEdit(''), name set to 'name'
    E('text')      ->   QLineEdit('text')
    C('text')      ->   QCheckBox('text')
    R('text')      ->   QRadioButton('text')
    HS('name')     ->   QSlider(Qt::Horizontal), name set to 'name'
    VS('name')     ->   QSlider(Qt::Horizontal), name set to 'name'
    Separator      ->   Horizontal separator
    VSeparator     ->   Vertical separator
    widget         ->   any valid QT widget is accepted
    (widget, name) ->   any valid QT widget, name set to 'name'
    _              ->   QLabel('')
    ___            ->   (three underscores) Horizontal widget span
    III            ->   (three capital letters i) vertical widget span

    QPushButtons with both image and text:
    ['image.jpg', 'text']  ->   QPushButton(QIcon('image.jpg'), 'text')
    B('image.jpg', 'text')      (name set to 'text')

Signals can be connected with gui.events() where every widget has:

    _                    = no connection
    slot                 = reference to Python callable, using the default
                          widget signal (if pre-defined, otherwise ValueError)
    ('textEdited', slot) = signal name, reference to Python callable.

'''

import re
import sys
import queue
import signal
import os.path
import functools
import contextlib
from enum import Enum
from types import SimpleNamespace
from collections import namedtuple, defaultdict
from collections.abc import Sequence, Mapping, MutableSequence

from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QAbstractSlider
from PyQt5.QtWidgets import QPushButton, QRadioButton, QCheckBox, QFrame
from PyQt5.QtWidgets import QLineEdit, QGridLayout, QSlider, QAbstractButton
from PyQt5.QtWidgets import QMessageBox, QListWidget, QAbstractItemView
from PyQt5.QtWidgets import QPlainTextEdit, QHBoxLayout
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QEvent

# We need a QApplication before creating any widgets
if QApplication.instance() is None:
    app = QApplication([])

# Needed in order for PyQt to play nice with Ctrl-C
signal.signal(signal.SIGINT, signal.SIG_DFL)

# Widget shortcuts

B = QPushButton
E = QLineEdit
C = QCheckBox
R = QRadioButton


def HS(name):
    '''Horizontal slider'''
    return (QSlider(Qt.Horizontal), name)


def VS(name):
    '''Vertical slider'''
    return (QSlider(Qt.Vertical), name)


class III:
    '''Vertical continuation'''
    pass


class _:
    '''Empty grid cell'''
    pass


class ___:
    '''Horizontal continuation'''
    pass


_specials = (_, ___, III)


def _sequence(x):
    return isinstance(x, Sequence) and not isinstance(x, str)


def _mutable_sequence(x):
    return isinstance(x, MutableSequence) and not isinstance(x, str)

############
# Property like get/set methods for fast widget access:
# value = gui.name calls get()
# gui.name = value calls set()
# We cannot use real properties because they are defined on the class
# and would be shared by different GUIs!

InstanceProperty = namedtuple('InstanceProperty', 'get set')


def _text_property(widget):
    '''Property for text-based widgets (labels, buttons)'''

    def get_text():
        return widget.text()

    def set_text(text):
        widget.setText(text)

    return InstanceProperty(get_text, set_text)


def _value_property(widget, typ):
    '''Property for value-based widgets (sliders)'''

    def get_value():
        return widget.value()

    def set_value(value):
        widget.setValue(typ(value))

    return InstanceProperty(get_value, set_value)


def _readonly_property(widget):
    '''Property for widgets that are not modifiable'''

    def getx():
        return widget

    return InstanceProperty(getx, None)


def _items_property(widget):
    '''Property for widgets with string lists'''

    def get_items():
        return map(lambda x: x.text(), widget.findItems("*", Qt.MatchWildcard))

    def set_items(lst):
        widget.clear()
        widget.addItems(map(str, lst))

    return InstanceProperty(get_items, set_items)


#########

class SmartQLabel(QWidget):
    '''A smarter QLabel that accepts strings, lists and dicts.

    Internally is a QHBoxLayout with two labels. The right label is
    usually hidden, and only the left label is used for simple strings
    and lists, which are shown one element per line.
    If a dict is passed, both labels are shown and used for keys and
    values respectively, one element per line.
    '''

    def __init__(self, text=''):

        super().__init__()
        self._layout = QHBoxLayout()
        self._left = QLabel('')
        self._right = QLabel('')
        self._layout.addWidget(self._left)
        self._layout.addWidget(self._right)
        self.setLayout(self._layout)
        self.setText(text)

    def setText(self, value):

        if isinstance(value, Mapping):
            keys = [str(x).strip() for x in value.keys()]
            values = [str(x).strip() for x in value.values()]
            self._left.setText('\n'.join(keys))
            self._right.setText('\n'.join(values))
            self._right.show()

        elif _sequence(value):
            self._right.hide()
            lines = [str(x).strip() for x in value]
            self._left.setText('\n'.join(lines))

        else:
            self._right.hide()
            self._left.setText(str(value))

        self._orig_value = value

    def text(self):
        return self._orig_value


def _fake_property(widget):
    '''Create the instance property corresponding to `widget`'''

    if isinstance(widget, (QLabel, QAbstractButton, QLineEdit, SmartQLabel)):
        return _text_property(widget)

    elif isinstance(widget, QAbstractSlider):
        return _value_property(widget, int)

    elif isinstance(widget, QAbstractItemView):
        return _items_property(widget)

    else:
        return _readonly_property(widget)


########
# Widgets create with the special syntax. We need to make a new instance
# every time one is requested, otherwise we risk cross-window connections.

class _DeferredCreationWidget:
    '''Widget that will be created during Gui.__init__'''

    def create(self):
        pass


def _image_fullpath(gui, filename):
    '''Returns the full image path if the filename is valid, otherwise None'''

    if not os.path.isabs(filename):
        fullpath = os.path.join(gui.images_dir, filename)

    name, _ = os.path.splitext(filename)

    if os.path.exists(fullpath):
        return fullpath, name
    else:
        return None, name


class L(_DeferredCreationWidget):
    '''Text label or image label'''

    def __init__(self, text_or_filename):
        self._text_or_filename = text_or_filename

    def create(self, gui):
        fullpath, name = _image_fullpath(gui, self._text_or_filename)
        if fullpath:
            label = QLabel()
            label.setPixmap(QPixmap(fullpath))
            return (label, name)
        else:
            return (SmartQLabel(self._text_or_filename), name)


class B(_DeferredCreationWidget):
    '''Text button or image+optional text button'''

    def __init__(self, text_or_filename, text=''):
        self._text_or_filename = text_or_filename
        self._text = text

    def create(self, gui):
        fullpath, name = _image_fullpath(gui, self._text_or_filename)
        if fullpath:
            return (QPushButton(QIcon(fullpath), self._text), name)
        else:
            return (QPushButton(self._text_or_filename), name)


class _AutoConnectButton(_DeferredCreationWidget):

    def __init__(self, text, slot_name):
        self._text = text
        self._slot_name = slot_name

    def create(self, gui):
        button = QPushButton(self._text)
        slot = getattr(gui, self._slot_name)
        handler = _exception_wrapper(slot, gui._exception_mode)
        button.clicked.connect(handler)
        return button


Exit = _AutoConnectButton('Exit', 'close')
Quit = _AutoConnectButton('Quit', 'close')
Close = _AutoConnectButton('Close', 'close')
Ok = _AutoConnectButton('Ok', 'close')
Cancel = _AutoConnectButton('Cancel', 'close')
Yes = _AutoConnectButton('Yes', 'close')
No = _AutoConnectButton('No', 'close')


class _Separator(_DeferredCreationWidget):
    '''horizontal or vertical seperator'''

    def __init__(self, linetype):
        self._linetype = linetype

    def create(self, gui):
        frame = QFrame()
        frame.setFrameShadow(QFrame.Sunken)
        frame.setFrameShape(self._linetype)
        if self._linetype == QFrame.HLine:
            frame.setMinimumWidth(1)
            frame.setFixedHeight(10)
        else:
            frame.setMinimumHeight(1)
            frame.setFixedWidth(10)
        return frame


Separator = _Separator(QFrame.HLine)
VSeparator = _Separator(QFrame.VLine)


#################
# List box

class QListWidgetWithDropSignal(QListWidget):
    '''A QListWidget that emits a signal when something is dropped on it.'''

    dropped = pyqtSignal()

    def dropEvent(self, event):
        super().dropEvent(event)
        self.dropped.emit()


def LB(name):
    '''Listbox'''
    return (QListWidgetWithDropSignal(), name)


#################
# Slider combined with editbox

class QLineEditDoNotErase(QLineEdit):
    '''A QLineEdit that whose contents must not be erased

    Gui constructor erases all the QLineEdit content because normally
    it is the widget name. This class signals that the contents should
    not be erased.
    '''
    pass


class CombinedWidget:
    '''Base class for widgets that combine multiple ones'''
    pass


class _ValueSlider(CombinedWidget):
    '''A slider combined with an inputbox for the value.'''

    def __init__(self, orientation,
                      name,
                      anchor,
                      myrange=None,
                      unit='',
                      default=None):

        if myrange is None:
            myrange = range(0, 100, 1)
        if unit != '':
            unit = ' ' + unit

        start, stop, step = myrange.start, myrange.stop, myrange.step

        # Normalize things to step of 1
        factor = 1.0 / step
        step = 1
        start *= factor
        stop *= factor

        slider = QSlider(orientation)
        slider.setMinimum(start)
        slider.setMaximum(stop)
        slider.setSingleStep(step)

        editbox = QLineEditDoNotErase()

        def slider_to_unit(v):
            return v / factor

        def unit_to_slider(v):
            return v * factor

        def update_editbox(value):
            editbox.setText(str(slider_to_unit(value)) + unit)

        def update_slider():
            text = editbox.text()
            pattern = r'^\s*(\d+)'
            m = re.search(pattern, text)
            if m:
                value = m.group(1)
                slider.setValue(unit_to_slider(float(value)))

        slider.valueChanged.connect(update_editbox)
        editbox.returnPressed.connect(update_slider)

        if default is None:
            slider.setValue(start)
        else:
            slider.setValue(unit_to_slider(default))

        self.slider = slider
        self.editbox = editbox
        self.anchor = anchor
        self.name = name

    def place(self, lol, row, col):

        if self.anchor == Qt.AnchorLeft or self.anchor == Qt.AnchorTop:
            first, last = self.editbox, (self.slider, self.name)
        else:
            first, last = (self.slider, self.name), self.editbox

        if self.slider.orientation() == Qt.Horizontal:
            ncols = len(lol[row])
            cells = [col]
            for n in range(col+1, ncols):
                if lol[row][n] == ___:
                    cells.append(n)
            if len(cells) < 2:
                raise ValueError('HValueSlider needs at least '
                                 'one horizontal continuation')

            lol[row][cells[0]] = first
            for n in cells[1:-1]:
                lol[row][n] = self.slider
            lol[row][cells[-1]] = last

        else:
            nrows = len(lol)
            cells = [row]
            for n in range(row+1, nrows):
                if lol[n][col] == III:
                    cells.append(n)
            if len(cells) < 2:
                raise ValueError('VValueSlider needs at least '
                                 ' one vertical continuation')

            lol[cells[0]][col] = first
            for n in cells[1:-1]:
                lol[n][col] = self.slider
            lol[cells[-1]][col] = last


def HValueSlider(name, myrange=None, unit='',
                 anchor=Qt.AnchorRight, default=None):
    '''A slider combined with an inputbox for the value.'''

    return _ValueSlider(Qt.Horizontal, name, anchor, myrange, unit, default)


def VValueSlider(name, myrange=None, unit='',
                 anchor=Qt.AnchorBottom, default=None):
    '''A slider combined with an inputbox for the value.'''

    return _ValueSlider(Qt.Vertical, name, anchor, myrange, unit, default)


#########
# Signals

_default_signals = {QPushButton: 'clicked',
                    QLineEdit: 'returnPressed',
                    QCheckBox: 'stateChanged',
                    QSlider: 'valueChanged',
                    QListWidgetWithDropSignal: 'currentTextChanged'}

Event = namedtuple('Event', 'signal args')


# Empty queue exception for get()

class Empty(Exception):
    '''Empty queue exception'''
    pass


#####################
# Exception handling

class Exceptions(Enum):
    '''Enum type for exceptions handling'''

    # Do not use auto() becase it requires python3.6

    OFF = 1                 # Do not catch exceptions
    SILENT = 2              # Discard all exceptions silently
    POPUP = 3               # Popup error string
    PRINT = 4               # Print error string to stdout
    pass                    # callable = custom exception handler


def _exception_wrapper(func, mode):
    if mode == Exceptions.OFF:
        return func

    elif mode == Exceptions.SILENT:
        handler = lambda e: None

    elif mode == Exceptions.PRINT:
        handler = lambda e: print('Exception: %s\n%s' %
                                  (e.__class__.__name__, str(e)))

    elif mode == Exceptions.POPUP:
        handler = lambda e: QMessageBox.warning(None, "Error", "%s\n%s" %
                                                (e.__class__.__name__, str(e)))
    elif callable(mode):
        handler = mode

    else:
        raise TypeError('Exception mode must be either an instance of '
                        'the Exceptions enum or a callable handler.')

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            handler(e)

    return wrapper


############
# Matplotlib

class MatplotlibWidget:
    '''Dummy definition to avoid importing matplotlib when it is not used.'''
    pass


@contextlib.contextmanager
def Ax(widget):
    '''
    Context manager to help drawing on Matplotlib widgets.

    Takes care of clearing and redrawing the canvas before and after
    the inner code block is executed.

    usage:
        with MatplotlibAx(gui.plot) as ax:
            ax.plot(...)
    '''
    if not isinstance(widget, MatplotlibWidget):
        raise TypeError('An instance of MatplotlibWidget is required, '
                        'got %s instead' % widget.__class__.__name__)
    ax = widget.ax
    ax.clear()

    yield ax

    ax.figure.canvas.draw()


def M(name, width=5, height=3, dpi=100):
    '''Returns a Matplotlib Canvas widget'''

    if globals()['MatplotlibWidget'].__name__ == 'MatplotlibWidget':

        from matplotlib.figure import Figure
        from matplotlib.backends.backend_qt5agg import FigureCanvas

        class RealMatplotlibWidget(FigureCanvas):
            def __init__(self, width, height, dpi):
                figure = Figure(figsize=(width, height), dpi=dpi)
                self.ax = figure.add_subplot(111)
                super().__init__(figure)

        globals()['MatplotlibWidget'] = RealMatplotlibWidget

    widget = MatplotlibWidget(width, height, dpi)
    return (widget, name)


#####################
# Stdout redirection

class StdoutLog(QPlainTextEdit):
    '''Log widget showing the stdout/stderr in the GUI'''

    newData = pyqtSignal(str)

    def __init__(self):
        super().__init__('')
        self.setReadOnly(True)

        # We replace just the write method and not the whole stdout/stderr,
        # because if the logging module is used, it makes a copy of
        # sys.stderr and the replacement would not work!

        sys.stdout.write = self._write
        sys.stderr.write = self._write

        self.newData.connect(self.dataAvail)

    # The write replacement uses a signal/slot instead of directly
    # writing to the widget in order to be thread-safe.

    def _write(self, data):
        self.newData.emit(data)

    def dataAvail(self, data):
        text = data.strip()
        if text != '':
            self.appendPlainText(text)


# Some helper functions


def _enumerate_lol(lol, skip_specials=True):
    '''
    Enumerate a list of lists in 2d. Usage::

        for row, column, element in _enumerate_lol(lists)
    '''
    for i, row in enumerate(lol):
        for j, element in enumerate(row):
            if skip_specials and element in _specials:
                continue
            yield i, j, element


def _normalize(x):
    '''Return x without all special characters. Keep only a-zA-Z0-9 and _'''
    return ''.join(c for c in x if c.isalnum() or c == '_')


def _bound_method(method, to_whom):
    '''Return True is `method` is bound to `to_whom`'''
    return hasattr(method, '__self__') and method.__self__ == to_whom


def _filter_lol(lol, func):
    '''Apply func to all elements in a list of lists'''
    for row in lol:
        for i in range(len(row)):
            row[i] = func(row[i])


def _check_widget(x):
    '''Check that x is a valid widget specification'''

    if (type(x) == tuple) and (len(x) == 2) and \
       isinstance(x[0], (QWidget, CombinedWidget)) and \
       isinstance(x[1], str):
        return x

    if isinstance(x, (QWidget, CombinedWidget)) or (x in _specials):
        return x

    raise ValueError('Element ' + str(x) + ' must be a widget '
                     'or a (widget, name) tuple')


def _process_slots(x):
    '''Normalize slots assignments.

    A callable is transformed into ('default', callable). The callable
    may be None to set it to the default get() handler.
    Tuples already in that format are type-checked.
    Specials (_, ___, III) are untouched.
    Other things raise a ValueError.
    '''
    if x in _specials:
        return x
    elif callable(x):
        return ('default', x)
    elif _sequence(x) and isinstance(x[0], str) and callable(x[1]):
        return x
    elif _sequence(x) and isinstance(x[0], str) and (x[1] is None):
        return x
    else:
        raise ValueError('Element %s is not a valid slot assignment' % x)


def _check_string(x):
    if not isinstance(x, str) and x not in _specials:
        raise TypeError('Element %s is not a string' % str(x))
    return x


def _create_deferred(gui, x):
    '''Create the instances of _DeferredCreationWidget'''

    if isinstance(x, _DeferredCreationWidget):
        return x.create(gui)

    elif isinstance(x, tuple) and len(x) == 2:
        return (_create_deferred(gui, x[0]), x[1])

    else:
        return x


def _collapse_names(x, first=True):
    '''((widget, name1), name2) -> (widget, name2), arbitrarily nested'''

    if not isinstance(x, tuple) or len(x) != 2:
        return x

    if first:
        return (_collapse_names(x[0], first=False), x[1])
    else:
        return _collapse_names(x[0], first=False)


def _layer_check(lol):
    '''
    Check that arguments to __init__ and others is OK.

    1. Check that all elements are iterables
    2. Take the longest
    3. Expand single-elements ones to the longest using ___
    4. Check that all rows have the same length, raise ValueError if not.
    '''
    for row in lol:
        if not _mutable_sequence(row):
            raise TypeError('Arguments are not lists '
                            '(or other mutable iterables)')

    row_lengths = [len(row) for row in lol]
    ncols = max(row_lengths)

    for row in lol:
        if len(row) == 1:
            row += [___] * (ncols - len(row))

    for row in lol:
        if len(row) != ncols:
            raise ValueError('Row lengths differ:'
                             ' row has %d elements instead of %d' %
                             (len(row), ncols))


# Compact element processing

def _convert_compacts(x):
    '''
    Compact elements processing.

    Converts:
        '__xxx___' to QLineEdit('xxx')
        'xxx'     to L('xxx')
        ['xxx']   to B('xxx')
        ['xxx', 'yyy']   to B('xxx', 'yyy')

    L and B are used instead of QLabel and QPushButton in order to support
    images if xxx is a valid filename.
    Lists with zero length or longer than 2 elements raise a ValueError.
    '''

    if isinstance(x, str) and x.startswith('__') and x.endswith('__'):
        return QLineEdit(x[2:-2])

    elif isinstance(x, str):
        return L(x)

    elif isinstance(x, list) and isinstance(x[0], str):
        if len(x) == 1 or len(x) == 2:
            return B(*x)
        else:
            raise ValueError('Invalid syntax: ' + str(x))

    elif isinstance(x, tuple) and len(x) == 2:
        return (_convert_compacts(x[0]), x[1])

    else:
        return x  # No change


##################
# GUIs persistence
# The global list keeps references to all GUIs and allows them
# to remain open even after the function that created them exits.


_guis = []


def _add_to_persistence_list(gui):
    _guis.append(gui)


def _remove_from_persistence_list(gui):
    try:
        _guis.remove(gui)
    except ValueError:   # Not found
        pass


#######################
# Async processing

class _result_event(QEvent):
    '''Event used for callback processing'''

    def __init__(self, code, callback, args):
        QEvent.__init__(self, code)
        self.callback = callback
        self.args = args


def _background_processing(gui, func, callback, *args):

    result = func(*args)
    if callback:
        if not _sequence(result):
            result = (result,)
        app = QApplication.instance()
        args = (gui,) + result
        app.postEvent(app, _result_event(QEvent.User, callback, args))


def _customEvent(ev):
    '''Replacement of QApplication.customEvent()'''

    callback = ev.callback
    args = ev.args
    callback(*args)


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

    # Persistence settings
    PERSISTENT = 1
    DYNAMIC = 2

    def __init__(self, *lists, images_dir='.',
                               create_properties=True,
                               exceptions=Exceptions.POPUP,
                               persistence=PERSISTENT):

        # This line must be the first one in this method otherwise
        # __setattr__ does not work.
        self.__dict__['_fake_properties'] = {}

        self.userdata = SimpleNamespace()

        if persistence == self.PERSISTENT:
            _add_to_persistence_list(self)

        self._layout = QGridLayout()
        self._widgets = {}                # widgets by name
        self._counter = defaultdict(int)  # widgets counter
        self._window = None
        self._app = QApplication.instance()

        self._get_handler = False   # These three for the get() method
        self._event_queue = queue.Queue()
        self._closed = False
        self._inverted = False
        self._exception_mode = exceptions
        self._create_properties = create_properties

        self.images_dir = images_dir

        # Input argument checks
        _layer_check(lists)
        _filter_lol(lists, _convert_compacts)
        _filter_lol(lists, functools.partial(_create_deferred, self))
        _filter_lol(lists, _collapse_names)
        _filter_lol(lists, _check_widget)

        # Intermediate step that will be filled by replicating
        # widgets when ___ and III are encountered.
        step1 = [[None] * len(lists[0]) for i in range(len(lists))]

        # Expand the combined widgets
        for i, j, element in _enumerate_lol(lists, skip_specials=False):
            if isinstance(element, CombinedWidget):
                element.place(lists, i, j)  # This modifies lists

        # Expand remaining ___ and 'III' replicating
        # the widgets from the previous column and row.
        for i, j, element in _enumerate_lol(lists, skip_specials=False):
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
                if element is None:
                    raise ValueError('Continuation from empty grid cell')

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
                if isinstance(widget, QLineEdit):
                    if not isinstance(widget, QLineEditDoNotErase):
                        widget.setText('')

                done.add(element)

        self.align_fake_properties()

    def align_fake_properties(self):
        '''Make sure that any and all widgets have a property'''

        self._fake_properties.clear()
        if self._create_properties:
            for name, widget in self._widgets.items():
                self._fake_properties[name] = _fake_property(widget)

    @property
    def widgets(self):
        '''Read-only property with the widgets dictionary'''
        return self._widgets

    def __getattr__(self, name):
        '''Use fake_properties to emulate properties on this instance'''

        if name in self.__dict__['_fake_properties']:
            return self.__dict__['_fake_properties'][name].get()

        # Default behaviour
        raise AttributeError(name)

    def __setattr__(self, name, value):
        '''Use fake_properties to emulate properties on this instance'''

        if name in self.__dict__['_fake_properties']:
            self.__dict__['_fake_properties'][name].set(value)
            return

        # Default behaviour
        super().__setattr__(name, value)

    def _get_widget_and_name(self, element):
        '''Fish out the widget and its name from a declaration.

        Several possibilities:
            - (widget, 'name')  - type checks should have already been
                                  performed before, hopefully
            - widget            - if widget defines text(), use that as
                                  its name, otherwise use the class name

        - remove special characeters, only leave a-zA-Z0-9
        - auto-number duplicate names.
        '''
        if isinstance(element, tuple):
            widget, name = element
        else:
            widget = element
            if hasattr(widget, 'text'):
                name = widget.text()
            else:
                name = widget.__class__.__name__

        name = _normalize(name)

        # If the name is a duplicate, auto-number it starting with 2.
        self._counter[name] += 1
        if self._counter[name] > 1:
            name = name + str(self._counter[name])

        return widget, name

    def row_stretch(self, *lists):
        '''Defines the row stretches'''

        _layer_check(lists)

        if len(lists) > self._layout.rowCount() or \
           len(lists[0]) != self._layout.columnCount():
            raise ValueError('Input arguments for row_stretch() must have '
                             'the same number of columns as the constructor '
                             'and as many or less lines')

        for i, j, stretch in _enumerate_lol(lists):
            self._layout.setRowStretch(i, stretch)

    def column_stretch(self, *lists):
        '''Defines the column stretches'''

        _layer_check(lists)

        if len(lists) > self._layout.rowCount() or \
           len(lists[0]) != self._layout.columnCount():
            raise ValueError('Input arguments for column_stretch() must have '
                             'the same number of columns as the constructor '
                             'and as many or less lines')

        for i, j, stretch in _enumerate_lol(lists):
            self._layout.setColumnStretch(j, stretch)

    def events(self, *lists):
        '''Defines the GUI events

        The argument must be a layout with the same shape as the
        initializer. Every element is a tuple with:

            ('signal_name', slot)

        where 'signal_name' is the name of the QT signal to be connected,
        and slot is any Python callable. Use _ for widgets that do not
        need to be connected to a slot.

        If just the default signal is wanted, 'signal_name' can be omitted
        and just the callable slot is required (without using a tuple).

        Bound methods are called without arguments. Functions and
        unbound methods will get a single argument with a reference
        to this Gui instance.
        '''
        _layer_check(lists)
        _filter_lol(lists, _process_slots)

        if len(lists) > self._layout.rowCount() or \
           len(lists[0]) != self._layout.columnCount():
            raise ValueError('Input arguments for values() must have the '
                             'same number of columns as the constructor and '
                             'as many or less lines')

        for i, j, pair in _enumerate_lol(lists):
            item = self[i,j]
            signal_name, slot = pair

            if signal_name == 'default':
                try:
                    signal_name = _default_signals[item.__class__]
                except KeyError as e:
                    raise ValueError('No default event for widget %s ' %
                                     str(item.__class__)) from e
            try:
                signal = getattr(item, signal_name)
            except AttributeError as e:
                raise ValueError('No signal %s found for widget %s' %
                                 (signal_name, str(item.__class__))) from e

            # Custom signal with default handler for get()
            if slot is None:
                slot = functools.partial(self._event_handler, signal, item)

            if _bound_method(slot, to_whom=self):
                use_slot = slot
            else:
                use_slot = functools.partial(slot, self)

            signal.connect(_exception_wrapper(use_slot, self._exception_mode))

    def rename(self, *lists):
        '''Overrides the default widget names

        The argument must be a layout with the same shape as the
        initializer. Every element is a string with the new name
        for the widget in that position.
        '''
        _layer_check(lists)
        _filter_lol(lists, _check_string)

        names_by_widget = {v: k for k, v in self._widgets.items()}

        for i, j, new_name in _enumerate_lol(lists):
            widget = self[i,j]
            old_name = names_by_widget[widget]

            self._widgets[new_name] = self._widgets[old_name]
            del self._widgets[old_name]

        self.align_fake_properties()

    def __getitem__(self, name):
        '''Widget by coordinates [row,col]'''
        return self._layout.itemAtPosition(name[0], name[1]).widget()

    def layout(self):
        '''Returns the Gui layout, containing all the widgets'''
        return self._layout

    def window(self):
        '''Builds a QT window containing all the Gui widgets and returns it'''
        if self._window is None:
            self._window = QWidget()
            self._window.setLayout(self._layout)
            self._window.closeEvent = self._close_handler
        return self._window

    def _close_handler(self, event):
        _remove_from_persistence_list(self)

    def import_into(self, obj):
        '''
        Add all widgets to `obj`.

        Adds all this Gui's widget to `obj` as new attributes.
        Typically used in classes
        as an alternative from deriving from Gui.
        Duplicate attributes will raise an AttributeError.
        '''
        for name, widget in self._widgets.items():
            if hasattr(obj, name):
                raise AttributeError('Cannot import: duplicate name ' + name)
            else:
                setattr(obj, name, widget)

    def run(self):
        '''Display the Gui and start the event loop.

        This call is blocking and will return when the window is closed.
        Any user interaction must be done with callbacks.
        '''
        self.show()
        self._app.exec_()

    def show(self):
        '''Shows the GUI. This call is non-blocking'''
        self.window().show()

    def close(self, dummy=None):    # Default argument for clicked(bool)
        '''Close the window'''
        if self._window:
            self._window.close()

    def _invert_dicts(self):
        if not self._inverted:
            self._names_by_widget = {v: k for k, v in self._widgets.items()}
            self._inverted = True

    def get(self, block=True, timeout=None):
        '''Runs the GUI in queue mode

        In queue mode, no callbacks are used. Insted, the user should call
        gui.get() in a loop to get the events and process them.
        The QT event loop will stop in between calls to gui.get(), so
        event processing should be quick.

        Every time an event happens, get() will return a tuple:

            name, event = gui.get()

        where `name` is widget name that generated the event, and event
        is a `namedtuple` with members `signal` (the PyQT signal)
        and `args` which is a list of signal arguments, which may be empty
        for signals without arguments.

        get() will return (None, None) after the gui is closed.
        '''
        if self._closed:
            return (None, None)

        self._invert_dicts()

        # Connect handler for all events
        if not self._get_handler:
            for widget in self._widgets.values():
                klass = widget.__class__
                if klass in _default_signals:
                    signal = getattr(widget, _default_signals[klass])
                    handler = functools.partial(self._event_handler,
                                                signal,
                                                widget)
                    signal.connect(handler)
            self._get_handler = True

        self.window().closeEvent = self._stop_handler
        self.show()
        self._closed = False

        if (block is False) or (timeout is not None):
            if (block is False) or (timeout < 0):
                timeout = 0
            QTimer.singleShot(timeout * 1000,
                              Qt.PreciseTimer,
                              self._timeout_handler)

        self._app.exec_()  # Start event loop. Handlers will stop it

        signal, widget, *args = self._event_queue.get()
        if signal == 'timeout':
            raise Empty
        elif signal is None:
            self._closed = True
            return (None, None)
        else:
            name = self._names_by_widget[widget]
            return (name, Event(signal, args))

    def _event_handler(self, signal, widget, *args):
        self._event_queue.put((signal, widget, *args))
        self._app.exit()  # Stop event loop

    def _stop_handler(self, event):
        self._event_queue.put((None, None, None))
        self._app.exit()  # Stop event loop
        _remove_from_persistence_list(self)

    def _timeout_handler(self):
        self._event_queue.put(('timeout', None, None))
        self._app.exit()  # Stop event loop

    def execute_in_background(self, func, args=(), callback=None):
        '''
        Executes `func` in a background thread and updates GUI with a callback.

        When func is done, the callback is called in the GUI thread.
        The callback receives a reference to this Gui instance as the first
        argument, plus whatever was returned by `func` as additional
        arguments.
        '''
        import threading

        if not callable(func):
            raise TypeError('func must be a callable')
        if not callable(callback):
            raise TypeError('callback must be a callable')

        app = QApplication.instance()
        app.customEvent = _customEvent

        t = threading.Thread(target=_background_processing,
                             args=(self, func, callback, *args))
        t.start()

    def enable_drag_and_drop(self, from_, to):
        '''Enable drag and drop between the two widgets'''

        self.widgets[from_].setDragEnabled(True)
        self.widgets[to].setAcceptDrops(True)

    def get_selections(self, name):

        widget = self.widgets[name]

        if hasattr(widget, 'selectedItems'):
            return map(lambda x: x.text(), widget.selectedItems())

        elif hasattr(widget, 'selectedText'):
            return widget.selectedText()

        else:
            raise TypeError('Widget %s has no selection methods' % widget)

# ___oOo___
