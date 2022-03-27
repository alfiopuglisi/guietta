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
    '__name__:text'->   QLineEdit('text'), name set to 'name'
    E('text')      ->   QLineEdit('text')
    C('text')      ->   QCheckBox('text')
    R('text')      ->   QRadioButton('text')
    HS('name')     ->   QSlider(Qt::Horizontal), name set to 'name'
    VS('name')     ->   QSlider(Qt::Horizontal), name set to 'name'
    HSeparator     ->   Horizontal separator
    VSeparator     ->   Vertical separator
    widget         ->   any valid QT widget is accepted
    (widget, name) ->   any valid QT widget, name set to 'name'
    _              ->   QLabel('')
    ___            ->   (three underscores) Horizontal widget span
    III            ->   (three capital letters i) vertical widget span
    M              ->   Matplotlib plot or image
    MA             ->   Matplotlib plot or imag with fast update
    PG             ->   pyqtgraph plot
    PGI            ->   pyqtgraph image

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
import ast
import sys
import queue
import signal
import inspect
import os.path
import textwrap
import functools
import threading
import contextlib
from enum import Enum
from types import SimpleNamespace
from functools import wraps
from collections import namedtuple, defaultdict
from collections.abc import Sequence, Mapping, MutableSequence

try:
    from PySide2.QtWidgets import QApplication, QLabel, QWidget, QAbstractSlider
    from PySide2.QtWidgets import QPushButton, QRadioButton, QCheckBox, QFrame
    from PySide2.QtWidgets import QLineEdit, QGridLayout, QSlider, QAbstractButton
    from PySide2.QtWidgets import QMessageBox, QListWidget, QAbstractItemView
    from PySide2.QtWidgets import QPlainTextEdit, QHBoxLayout, QComboBox
    from PySide2.QtWidgets import QSplashScreen, QFileDialog, QButtonGroup
    from PySide2.QtWidgets import QProgressBar, QGroupBox
    from PySide2.QtGui import QPixmap, QIcon, QFont
    from PySide2.QtCore import Qt, QTimer, Signal, QEvent
except ImportError:
    try:
        from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QAbstractSlider
        from PyQt5.QtWidgets import QPushButton, QRadioButton, QCheckBox, QFrame
        from PyQt5.QtWidgets import QLineEdit, QGridLayout, QSlider, QAbstractButton
        from PyQt5.QtWidgets import QMessageBox, QListWidget, QAbstractItemView
        from PyQt5.QtWidgets import QPlainTextEdit, QHBoxLayout, QComboBox
        from PyQt5.QtWidgets import QSplashScreen, QFileDialog, QButtonGroup
        from PyQt5.QtWidgets import QProgressBar, QGroupBox
        from PyQt5.QtGui import QPixmap, QIcon, QFont
        from PyQt5.QtCore import Qt, QTimer, QEvent
        from PyQt5.QtCore import pyqtSignal as Signal
    except ImportError as e:
        raise Exception('At least one of PySide2 or PyQt5 must be installed') from e

# We need a QApplication before creating any widgets
if QApplication.instance() is None:
    app = QApplication([])

# Needed in order for PyQt to play nice with Ctrl-C
signal.signal(signal.SIGINT, signal.SIG_DFL)

# Widget shortcuts

E = QLineEdit
C = QCheckBox
R = QRadioButton
G = QGroupBox


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


#########
# Context managers

class ContextMixIn():
    '''Mixin class to allow a widget to be used with the `with` statement.

    The with code block is used to compile a function that will be connected
    to the widget's default signal.
    '''

    def __enter__(self):
        self._start = inspect.stack()[1]
        return self

    def __exit__(self, *args):
        end = inspect.stack()[1]

        if end.filename == '<stdin>':
            import readline
            idx = readline.get_current_history_length()
            withlines = []
            while True:
                line = readline.get_history_item(idx)
                withlines.insert(0, line)
                if line.strip().startswith('with'):
                    break
                idx -= 1
        else:
            # Do not use inspect.getsourcelines because it appears
            # to fail on some systems
            lines = open(self._start.filename).readlines()
            withlines = lines[self._start.lineno - 1 : end.lineno]

        withsource = textwrap.dedent(''.join(withlines))

        tree = ast.parse(withsource)
        analyzer = _Analyzer()
        analyzer.visit(tree)
        gui_name = analyzer.gui_name

        if gui_name is None:
            raise ValueError('Could not determine the Gui instance identifier')

        slotlines = withlines[1:]
        slotsource = textwrap.dedent(''.join(slotlines))

        code = 'def slot(%s, *args):\n' % gui_name
        code += textwrap.indent(slotsource, ' ')
        caller_locals = inspect.stack()[1].frame.f_locals
        caller_globals = inspect.stack()[1].frame.f_globals

        # heed the Python docs warning about modifying locals()
        locals_copy = caller_locals.copy()
        exec(code, caller_globals, locals_copy)

        if hasattr(self, '_widget'):
            widget = self._widget
        else:
            widget = self

        connect(widget, slot=locals_copy['slot'])

        return True   # Cancel the exception raised by the first execution

    @classmethod
    def convert_object(cls, obj):
        '''Add this class as a mixin after an object has been created'''

        base_cls = obj.__class__
        base_cls_name = obj.__class__.__name__
        new_name = 'Context' + base_cls_name
        obj.__class__ = type(new_name, (base_cls, cls), {})


class _Analyzer(ast.NodeVisitor):
    '''
    AST analyzer that detects all instances of attribute access like::

        a = gui.widget
    '''

    def __init__(self, decorator_name='auto'):
        self.gui_name = None
        self.accessed_widgets = set()
        self.decorator_name = decorator_name

    def visit_Attribute(self, node):
        '''Detect all reads like "gui.widget"'''

        if (
            isinstance(node.value, ast.Name)
            and node.value.id == self.gui_name
            and isinstance(node.ctx, ast.Load)
            and node.attr != self.decorator_name
        ):
            self.accessed_widgets.add(node.attr)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        '''Detect "gui" in "@gui.auto"'''

        decorators = node.decorator_list
        for d in decorators:
            if (
                isinstance(d, ast.Attribute)
                and d.attr == self.decorator_name
            ):
                self.gui_name = d.value.id
        self.generic_visit(node)

    def visit_With(self, node):
        '''Detect "gui" in "with gui.widget'''

        for item in node.items:
            if isinstance(item.context_expr, ast.Attribute):
                self.gui_name = item.context_expr.value.id
        self.generic_visit(node)


############
# Property like get/set methods for fast widget access:
# value = gui.name calls get()
# gui.name = value calls set()
# We cannot use real properties because they are defined on the class
# and would be shared by different GUIs!

class GuiettaProperty:
    '''Holds the get/set methods for a Guietta magic property.
    
    Initialize with two callables, *get* and *set()*::

        get() - returns the property value
        set(x) - sets the property to x

    *widget* must be a reference to the widget for which the property is
    being set.
    
    The *set()* method is automatically decorated with
    `guietta.execute_in_main_thread` and `guietta.undo_context_manager`.
    Set *add_decorators* to False to avoid this. In this case, the
    *widget* parameter is ignored.
    '''
    def __init__(self, get, set, widget, add_decorators=True):
        try:
            assert(callable(get))
            assert(callable(set))
        except AssertionError as e:
            errmsg = 'get and set must be two Python callables'
            raise TypeError(errmsg) from e
            
        self.get = get
        if add_decorators:
            gui = widget._gui
            set = undo_context_manager(get)(execute_in_main_thread(gui)(set))
        self.set = set


class _ContextStr(str, ContextMixIn):
    def __new__(cls, widget, *args, **kw):
        return str.__new__(cls, *args, **kw)

    def __init__(self, widget, *args, **kwargs):
        self._widget = widget


class _ContextInt(int, ContextMixIn):
    def __new__(cls, widget, *args, **kw):
        return int.__new__(cls, *args, **kw)

    def __init__(self, widget, *args, **kwargs):
        self._widget = widget


class _ContextList(list, ContextMixIn):

    def __init__(self, widget, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._widget = widget


class _ContextDict(dict, ContextMixIn):

    def __init__(self, widget, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._widget = widget


def _alsoAcceptAnotherGui(widget):
    '''Decorator for the set() function of a guietta property.

    Adds the possibility of receiving a Gui instance as the value,
    replacing the widget with the Gui widget. In case of the widget
    is a QGroupBox instance, the GUi is placed as the inner layout instead.
    '''
    def decorator(f):
        @wraps(f)
        def wrapper(value):
            if isinstance(value, Gui):
                if isinstance(widget, QGroupBox):
                    widget.setLayout(value.layout())
                else:
                    widget._gui.layout().replaceWidget(widget, value.window())
                    widget.hide()
                widget._gui.add_as_subgui(value)
            else:
                f(value)
        return wrapper
    return decorator


def undo_context_manager(get_func):
    '''
    Modify the decorated function so that it returns a context manager that,
    when exiting, restores the previous widget state (saved
    calling *get_func*)::
        
        def get_label()
            return gui.label

        @undo_context_manager(get_label):
        def set_label(value):
            gui.label = value
            
    then later in the program::
        
        with set_label(value):
            ...
    
    upon exiting the *with* block, the label text will revert to its
    previous value.
    '''
    def decorator(f):
        @wraps(f)
        def wrapper(value):

            class InnerUndoContextManager:
                def __init__(self, old_value):
                    self.old_value = old_value
                def __enter__(self): pass
                def __exit__(self, *args):
                    f(self.old_value)

            old_value = get_func()
            f(value)
            return InnerUndoContextManager(old_value)

        return wrapper
    return decorator


def execute_in_main_thread(gui):
    '''Decorator that makes sure that GUI methods run in the main thread.
    
    QT restricts GUI updates to the main thread (that is, the thread that
    created the GUI). In order to allow updating
    the GUI from other threads, any function that does so can be decorated::
        
        @execute_in_main_thread(gui)
        def myfunc(gui, widget, text):
           widget.setText(text)

    The decorator checks the current thread and, if different from the
    main GUI thread, wraps the function call into a QT event that will
    be eventually received and processed by the main GUI thread. Otherwise,
    the function is executed immediately.
    
    All guietta magic properties already use this decorator, so all GUI
    updates are automatically executed in the main GUI thread.
    '''
    def decorator(f):
        @wraps(f)
        def wrapper(*args):
            return gui.execute_in_main_thread(f, *args)

        return wrapper
    return decorator


def _signal_property(widget):
    '''Property that handles the widget's default signal

    Assign a callable to this property in order to connect a function
    as a slot for the widget default signal.
    '''
    def getx():
        return widget

    @_alsoAcceptAnotherGui(widget)
    def setx(value):
        connect(widget, slot=value)

    return GuiettaProperty(getx, setx, widget)


def _text_property(widget):
    '''Property for text-based widgets (labels, buttons)'''

    def get_text():
        text = widget.text()
        return _ContextStr(widget, text)

    @_alsoAcceptAnotherGui(widget)
    def set_text(text):
        if isinstance(widget, SmartQLabel):
            widget.setText(text)
        else:
            widget.setText(str(text))

    return GuiettaProperty(get_text, set_text, widget)


def _title_property(widget):
    '''Property for widgets with a title (QGroupBox)'''

    def get_title():
        title = widget.title()
        return _ContextStr(widget, title)

    @_alsoAcceptAnotherGui(widget)
    def set_title(title):
        print('set_title')
        widget.setTitle(str(title))

    return GuiettaProperty(get_title, set_title, widget)


def _value_property(widget, typ):
    '''Property for value-based widgets (sliders)'''

    def get_value():
        value = widget.value()
        if typ is int:
            return _ContextInt(widget, value)
        else:
            return value

    @_alsoAcceptAnotherGui(widget)
    def set_value(value):
        widget.setValue(typ(value))

    return GuiettaProperty(get_value, set_value, widget)


def _readonly_property(widget):
    '''Property for widgets that are not modifiable'''

    def getx():
        return widget

    @_alsoAcceptAnotherGui(widget)
    def setx(x):
        raise AttributeError('This property is read-only')

    return GuiettaProperty(getx, setx, widget)


def _items_property(widget):
    '''Property for widgets with string lists'''

    def get_items():
        items = map(lambda x: x.text(), widget.findItems("*", Qt.MatchWildcard))
        return _ContextList(widget, items)

    @_alsoAcceptAnotherGui(widget)
    def set_items(lst):
        widget.clear()
        widget.addItems(list(map(str, lst)))  # use list() to support
                                              # PySide v5.9

    return GuiettaProperty(get_items, set_items, widget)


def _combobox_property(widget):
    '''Property for comboboxes'''

    def get_items():
        texts = [widget.itemText(i) for i in range(widget.count())]
        data = [widget.itemData(i) for i in range(widget.count())]
        return _ContextDict(widget, zip(texts, data))

    @_alsoAcceptAnotherGui(widget)
    def set_items(dct):
        widget.clear()
        for k, v in dct.items():
            widget.addItem(k, v)

    return GuiettaProperty(get_items, set_items, widget)


#########

class SmartQLabel(QWidget):
    '''A smarter QLabel that accepts strings, lists and dicts.

    Internally it's a QHBoxLayout with two labels. The right label is
    usually hidden, and only the left label is used for simple strings
    and lists, which are shown one element per line.
    If a dict is passed, both labels are shown and used for keys and
    values respectively, one element per line.

    If the initializator contains a % character, it is interpreted
    as a format string that will be used as the format for later
    assignments. This behaviour can be turned off by setting
    gui.use_formats to False.
    '''

    def __init__(self, text=''):

        super().__init__()
        self._layout = QHBoxLayout()
        self._left = QLabel('')
        self._right = QLabel('')
        self._layout.addWidget(self._left)
        self._layout.addWidget(self._right)
        self.setLayout(self._layout)
        self._format = None
        self.setText(text)
        if '%' in text:
            self._format = text

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
            if self._format and self._gui.use_formats:
                self._left.setText(self._format % value)
            else:
                self._left.setText(str(value))

        self._orig_value = value

    def text(self):
        return self._orig_value

    def __guietta_property__(self):
        return _text_property(self)


def _guietta_property(widget):
    '''Create the instance property corresponding to `widget`'''

    if isinstance(widget, QAbstractButton):
        return _signal_property(widget)

    elif isinstance(widget, (QLabel, QLineEdit, SmartQLabel)):
        return _text_property(widget)

    elif isinstance(widget, QGroupBox):
        return _title_property(widget)

    elif isinstance(widget, (QAbstractSlider, QProgressBar)):
        return _value_property(widget, int)

    elif isinstance(widget, QAbstractItemView):
        return _items_property(widget)

    elif isinstance(widget, QComboBox):
        return _combobox_property(widget)

    else:
        return _readonly_property(widget)


########
# Widgets created with the special syntax. We need to make a new instance
# every time one is requested, otherwise we risk cross-window connections.

class _DeferredCreationWidget:
    '''Widget that will be created during Gui.__init__'''

    def __init__(self, name):
        self._name = name

    def create(self, gui):
        pass


class HS(_DeferredCreationWidget):
    '''Horizontal slider'''

    def create(self, gui):
        return (QSlider(Qt.Horizontal), self._name)


class VS(_DeferredCreationWidget):
    '''Vertical slider'''

    def create(self, gui):
        return (QSlider(Qt.Vertical), self._name)


class P(_DeferredCreationWidget):
    '''Progress bar'''

    def __init__(self, text):
        self._text = text

    def create(self, gui):
        return (QProgressBar(), self._text)


class _R(_DeferredCreationWidget):
    '''Radio button in a group'''

    _group = None

    def __init__(self, text, checked=False):
        self._text = text
        self._checked = checked

    def create(self, gui):
        button = QRadioButton(self._text)
        button.setChecked(self._checked)
        gui._groups[self._group].addButton(button)
        return (button, self._text)


class R0(_R):
    '''Radio button in pre-defined button group #0'''

    _group = 0


class R1(_R):
    '''Radio button in pre-defined button group #1'''

    _group = 1


class R2(_R):
    '''Radio button in pre-defined button group #2'''

    _group = 2


class R3(_R):
    '''Radio button in pre-defined button group #3'''

    _group = 3


class R4(_R):
    '''Radio button in pre-defined button group #4'''

    _group = 4


class R5(_R):
    '''Radio button in pre-defined button group #5'''

    _group = 5


class R6(_R):
    '''Radio button in pre-defined button group #6'''

    _group = 6


class R7(_R):
    '''Radio button in pre-defined button group #7'''

    _group = 7


class R8(_R):
    '''Radio button in pre-defined button group #8'''

    _group = 8


class R9(_R):
    '''Radio button in pre-defined button group #9'''

    _group = 9


def _image_fullpath(gui, filename):
    '''Returns the full image path if the filename is valid, otherwise None'''

    if not os.path.isabs(filename):
        fullpath = os.path.join(gui.images_dir, filename)
    else:
        fullpath = filename

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
        if callable(self._slot_name):
            slot = functools.partial(self._slot_name, gui)
        else:
            slot = getattr(gui, self._slot_name)
        handler = _exception_wrapper(slot, gui)
        button.clicked.connect(handler)
        return button


class Exit(_AutoConnectButton):
    '''Exit button'''

    def __init__(self, name='Exit'):
        super().__init__(name, 'close')


class Quit(_AutoConnectButton):
    '''Quit button'''

    def __init__(self, name='Quit'):
        super().__init__(name, 'close')


class Ok(_AutoConnectButton):
    '''Ok button'''

    def __init__(self, name='Ok'):
        super().__init__(name, 'close')


class Cancel(_AutoConnectButton):
    '''Cancel button'''

    def __init__(self, name='Cancel'):
        super().__init__(name, 'close')


class Yes(_AutoConnectButton):
    '''Yes button'''

    def __init__(self, name='Yes'):
        super().__init__(name, 'close')


class No(_AutoConnectButton):
    '''No button'''

    def __init__(self, name='No'):
        super().__init__(name, 'close')


class _Separator(_DeferredCreationWidget):
    '''horizontal or vertical seperator'''

    def __init__(self, linetype, name):
        self._linetype = linetype
        self._name = name

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
        return (frame, self._name)


class HSeparator(_Separator):
    '''Horizontal separator'''

    def __init__(self, name='hseparator'):
        super().__init__(QFrame.HLine, name)


class VSeparator(_Separator):
    '''Vertical separator'''

    def __init__(self, name='vseparator'):
        super().__init__(QFrame.VLine, name)


#################
# List box

class _QListWidgetWithDropSignal(QListWidget):
    '''A QListWidget that emits a signal when something is dropped on it.'''

    drop = Signal()

    def dropEvent(self, event):
        super().dropEvent(event)
        self.drop.emit()


class LB(_DeferredCreationWidget):
    '''Listbox'''

    def create(self, gui):
        return (_QListWidgetWithDropSignal(), self._name)


#######################
# Combobox

class CB(_DeferredCreationWidget):
    '''Combobox'''

    def __init__(self, name, list_or_dict):
        self._name = name
        self._list_or_dict = list_or_dict

    def create(self, gui):

        cb = QComboBox()
        if isinstance(self._list_or_dict, Mapping):
            for k, v in self._list_or_dict.items():
                cb.addItem(k, v)

        elif _sequence(self._list_or_dict):
            for v in self._list_or_dict:
                cb.addItem(v, None)
        else:
            raise TypeError('ComboBox initializer must be either a sequence '
                            'or a mapping')

        return (cb, self._name)


########################
# Password entry field

class PW(_DeferredCreationWidget):
    '''A password entry field'''

    def create(self, gui):
        widget = QLineEdit('')
        widget.setEchoMode(QLineEdit.Password)
        return (widget, self._name)


#################
# Slider combined with editbox


class _CombinedWidget:
    '''Base class for widgets that combine multiple ones'''
    pass


class _ValueSlider(_CombinedWidget):
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

        editbox = QLineEdit('')

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

    def place(self, rows, row, col):

        slider_name = (self.slider, self.name)

        if self.anchor in [Qt.AnchorLeft, Qt.AnchorTop]:
            first, last = self.editbox, slider_name
        else:
            first, last = slider_name, self.editbox

        if self.slider.orientation() == Qt.Horizontal:
            ncols = len(rows[row])
            cells = [col]
            for n in range(col+1, ncols):
                if rows[row, n] == ___:
                    cells.append(n)
            if len(cells) < 2:
                raise ValueError('HValueSlider needs at least '
                                 'one horizontal continuation')

            rows[row, cells[0]] = first
            for n in cells[1:-1]:
                rows[row, n] = slider_name
            rows[row, cells[-1]] = last

        else:
            nrows = len(rows)
            cells = [row]
            for n in range(row+1, nrows):
                if rows[n, col] == III:
                    cells.append(n)
            if len(cells) < 2:
                raise ValueError('VValueSlider needs at least '
                                 ' one vertical continuation')

            rows[cells[0], col] = first
            for n in cells[1:-1]:
                rows[n, col] = slider_name
            rows[cells[-1], col] = last


class HValueSlider(_ValueSlider):
    '''A slider combined with an inputbox for the value.'''

    def __init__(self, name, myrange=None, unit='',
                       anchor=Qt.AnchorRight, default=None):

        super().__init__(Qt.Horizontal, name, anchor, myrange, unit, default)


class VValueSlider(_ValueSlider):
    '''A slider combined with an inputbox for the value.'''

    def __init__(self, name, myrange=None, unit='',
                       anchor=Qt.AnchorBottom, default=None):

        super().__init__(Qt.Vertical, name, anchor, myrange, unit, default)


#########
# Signals

_default_signals = {QPushButton: 'clicked',
                    QLineEdit: 'returnPressed',
                    QCheckBox: 'stateChanged',
                    QRadioButton: 'toggled',
                    QAbstractSlider: 'valueChanged',
                    QListWidget: 'currentTextChanged',
                    QGroupBox: 'clicked',
                    QComboBox: 'currentTextChanged'}


def _default_signal_lookup(widget):
    '''Looks up the default signal for a widget that may be a derived class'''

    for base_class, signal_name in _default_signals.items():
        if isinstance(widget, base_class):
            return signal_name
    else:
        raise KeyError(widget.__class__.__name__)


Event = namedtuple('Event', 'signal args')


# Empty queue exception for get()

class Empty(Exception):
    '''Empty queue exception'''
    pass


#####################
# Exception handling

class Exceptions(Enum):
    '''Enum type for exceptions handling'''

    # Do not use auto() because it requires python3.6

    OFF = 1                 # Do not catch exceptions
    SILENT = 2              # Discard all exceptions silently
    POPUP = 3               # Popup error string
    PRINT = 4               # Print error string to stdout
    pass                    # callable = custom exception handler


def _exception_handler(e, gui):
    '''
    Exception handler for all automatic actions and
    signal slots. The exception moment is checked on the fly,
    and thus can be changed at runtime.
    '''
    mode = gui._exception_mode

    if mode == Exceptions.OFF:
        raise e from None

    elif mode == Exceptions.SILENT:
        pass

    elif mode == Exceptions.PRINT:
        print('Exception: %s\n%s' % (e.__class__.__name__, str(e)))

    elif mode == Exceptions.POPUP:
        QMessageBox.warning(None, "Error", "%s\n%s" %
                           (e.__class__.__name__, str(e)))
    elif callable(mode):
        mode()

    else:
        raise TypeError('Exception mode must be either an instance of '
                        'the Exceptions enum or a callable handler.')

def _exception_wrapper(func, gui):
    '''
    Wraps *func* with the default exception handler, based
    on the exception mode set by *gui* at the moment of handling.
    '''
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            _exception_handler(e, gui)

    return wrapper


############
# Matplotlib

@contextlib.contextmanager
def Ax(widget):
    '''
    Context manager to help drawing on Matplotlib widgets.

    Takes care of clearing and redrawing the canvas before and after
    the inner code block is executed::

        with Ax(gui.plot) as ax:
            ax.plot(...)
    '''
    from guietta.guietta_matplotlib import Colorbar
    try:
        ax = widget.ax
    except AttributeError as e:
        raise AttributeError('Class %s does not have an ''ax'' attribute.\n'
                      'Are you sure that you are referencing the correct plot?'
                       %  widget.__class__.__name__) from e
        
    # hack to remove all colorbars, in order to restore the ax geometry:
    # creating a colorbar will resize the ax, and creating a new one
    # will resize it further, unless the previous one has been removed.
    for child in ax.get_children():
        if isinstance(getattr(child, 'colorbar', None), Colorbar):
            child.colorbar.remove()

    ax.clear()

    yield ax

    for k,v in widget.kwargs.items():
        getattr(widget.ax, k).__call__(v)
    ax.figure.canvas.draw()


class M(_DeferredCreationWidget):
    '''A Matplotlib Canvas widget

    The **kwargs accepts additional keywords that will become function
    calls every time the Ax decorator is used. For example, adding the
    argument `set_ylabel='foo'`, will result in this function call:
    `ax.set_ylabel('foo')`
    
    Creating an object of this class will import the matplotlib module.
    '''
    def __init__(self, name, width=5, height=3, dpi=100,
                       subplots=(1,1), animated=False, **kwargs):

        self._name = name
        self._width = width
        self._height = height
        self._dpi = dpi
        self._subplots = subplots
        self._kwargs = kwargs
        self._animated = animated

    def create(self, gui):
        from guietta import guietta_matplotlib
        widget_class = guietta_matplotlib.MatplotlibWidget

        _default_signals[widget_class] = 'clicked'

        widget = widget_class(self._width, self._height, self._dpi,
                              self._subplots, self._animated, **self._kwargs)
        return (widget, self._name)


class MA(M):
    '''Animated Matplotlib widget

    First display works as usual. When new data is assigned to the widget,
    the set_ydata (for plots) or set_array (for images) method is called to
    update the display without redrawing the entire widget.
    '''
    def __init__(self, name, width=5, height=3, dpi=100,
                       subplots=(1,1), **kwargs):
        super().__init__(name, width, height, dpi, subplots, animated=True, **kwargs)


class PG(_DeferredCreationWidget):
    '''A pyqtgraph PlotWidget.
    
    Creating an object of this class will import the pyqtgraph module.'''

    _pyqtgraph_imported = False
    
    def __init__(self, name, **kwargs):

        self._name = name
        self._kwargs = kwargs

    def create(self, gui):
        from guietta import guietta_pyqtgraph
        widget =  guietta_pyqtgraph.PyQtGraphPlotWidget(**self._kwargs)
        return (widget, self._name)
      

class PGI(_DeferredCreationWidget):
    '''A pyqtgraph ImageView.
    
      Creating an object of this class will import the pyqtgraph module.'''

    def __init__(self, name, **kwargs):
        self._name = name
        self._kwargs = kwargs

    def create(self, gui):
        from guietta import guietta_pyqtgraph
        widget =  guietta_pyqtgraph.PyQtGraphImageView(**self._kwargs)
        return (widget, self._name)


#####################
# Stdout redirection

class StdoutLog(QPlainTextEdit):
    '''Log widget showing the stdout/stderr in the GUI

    By default, stdout/stderr is redirected just before
    setup() is called, while the original stdout/err is kept
    while the GUI is initialized.
    '''
    newData = Signal(str)
    active = False

    def __init__(self):
        super().__init__('')
        self.setReadOnly(True)

        # We replace just the write method and not the whole stdout/stderr,
        # because if the logging module is used, it makes a copy of
        # sys.stderr and the replacement would not work!

        self._orig = sys.stdout.write, sys.stderr.write
        sys.stdout.write = self._write
        sys.stderr.write = self._write

        self.newData.connect(self.dataAvail)

    # The write replacement uses a signal/slot instead of directly
    # writing to the widget in order to be thread-safe.

    def _write(self, data):
        self.newData.emit(data)

    def dataAvail(self, data):
        if self.active:
            text = data.strip()
            if text != '':
                self.appendPlainText(text)
        else:
            self._orig[0](data)


# Some helper functions

def normalized(name):
    '''Returns the given *name* without any special characters or spaces.

    Only a-zA-Z0-9 and _ will be kept
    '''
    return ''.join(c for c in name if c.isalnum() or c == '_')


def _bound_method(method, to_whom):
    '''Return True is `method` is bound to `to_whom`'''
    return hasattr(method, '__self__') and method.__self__ == to_whom


def _list_base_classes(cls):
    bases = list(cls.__bases__)
    for base in bases:
        bases.extend(_list_base_classes(base))
    return bases


def _create_default_widgets(x):
    '''If a widget class is specified, create one with a default name'''

    if isinstance(x, type):
        bases = _list_base_classes(x)
        if (
            QWidget in bases
            or _CombinedWidget in bases
            or _DeferredCreationWidget in bases
        ):
            return x()

    # Also recurse into (WidgetClass, 'name')
    if (
        type(x) is tuple
        and (len(x) == 2)
        and isinstance(x[1], str)
    ):
        return (_create_default_widgets(x[0]), x[1])

    return x


def _check_widget(x):
    '''Check that x is a valid widget specification'''

    if (
        type(x) == tuple
        and (len(x) == 2)
        and isinstance(x[0], (QWidget, _CombinedWidget))
        and isinstance(x[1], str)
    ):
        return x

    if isinstance(x, (QWidget, _CombinedWidget)) or (x in _specials):
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

def _process_font(x):
    '''Normalize font assignments.

    *x* must be either a QFont instance, a string with a font
    family name (.e.g 'Helvetica'), or a sequence with the QFont
    constructor elements: family string, point size, weight, and italic,
    int that order. All except the family string are optional, point size
    and weight ar integers, and italic is a boolean True/False. Use -1
    for arguments that must be left at their default value while specifying
    a subsequent argument. All these specifications are valid:

        - QFont('helvetica', pointSize=12)
        - 'helvetica'
        - ['Arial', -1, -1, False]
        - ('helvetica', 12, 1, True)
    '''
    if isinstance(x, QFont):
        return x

    if x in _specials:
        return x

    elif isinstance(x, str):
        return QFont(x)

    elif _sequence(x):
        try:
            return QFont(*x)
        except Exception as e:
            raise ValueError('%s rejected by QFont constructor' % x) from e
    else:
        raise TypeError('Element %s is not a valid font specification' % x)

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


class Rows:
    '''
    Represents a list of rows

    Used in the Gui constructor and several other methods
    '''

    def __init__(self, rows):
        self.check(rows)
        self.rows = rows

    def __getitem__(self, idx):
        if isinstance(idx, int):
            return self.rows[idx]
        elif len(idx) == 2:
            return self.rows[idx[0]][idx[1]]
        else:
            raise TypeError('Unsupported index type:', idx)

    def __setitem__(self, idx, value):
        if isinstance(idx, int):
            self.rows[idx] = value
        elif len(idx) == 2:
            self.rows[idx[0]][idx[1]] = value
        else:
            raise TypeError('Unsupported index type:', idx)

    def __len__(self):
        return len(self.rows)

    def copy(self, init=None):
        rows = [[None] * len(self.rows[0]) for i in range(len(self.rows))]
        return Rows(rows)

    @staticmethod
    def check(rows):
        '''
        Check rows have the correct format:

        1. All rows must be iterables
        2. With the same length, or with a single element that will be
           expanded using ___
        '''

        for row in rows:
            if not _mutable_sequence(row):
                raise TypeError('Not all rows are not lists '
                                '(or other mutable iterables)')

        row_lengths = [len(row) for row in rows]
        ncols = max(row_lengths)

        for row in rows:
            if len(row) == 1:
                row += [___] * (ncols - len(row))

        for row in rows:
            if len(row) != ncols:
                raise ValueError('Row lengths differ:'
                                 ' row has %d elements instead of %d' %
                                 (len(row), ncols))

    def check_same(self, other, allow_less_rows=True):

        nrows1 = len(self.rows)
        nrows2 = len(other.rows)

        if nrows1 > nrows2:
            raise ValueError('Too many rows')

        if nrows1 < nrows2 and not allow_less_rows:
            raise ValueError('Too few rows')

        for row1, row2 in zip(self.rows, other.rows):
            if len(row1) != len(row2):
                raise ValueError('Row lengths differ')

    def enumerate(self, skip_specials=True):
        '''
        Enumerate in 2d. Usage::

            for row, column, element in rows.enumerate():
        '''
        for i, row in enumerate(self.rows):
            for j, element in enumerate(row):
                if skip_specials and element in _specials:
                    continue
                yield i, j, element

    def map_in_place(self, func):
        '''Apply func to all elements'''
        for row in self.rows:
            for i in range(len(row)):
                row[i] = func(row[i])


# Compact element processing

def _convert_compacts(x):
    '''
    Compact elements processing.

    Converts:
        '__xxx__:yy' to (QLineEdit('yy'), 'xxx')
        '__xxx__' to (QLineEdit(''), 'xxx')
        'xxx'     to L('xxx')
        ['xxx']   to B('xxx')
        ['xxx', 'yyy']   to B('xxx', 'yyy')
        callable  to button(x.__name__)

    L and B are used instead of QLabel and QPushButton in order to support
    images if xxx is a valid filename.
    Lists with zero length or longer than 2 elements raise a ValueError.
    A callable is converted to a button with text set to the callable's name,
    and the callable itself as the button slot.
    '''

    if isinstance(x, str):
        m = re.match(r'__(\w+)__\:(.*)', x)
        if m:
            return (QLineEdit(m.group(2)), m.group(1))

        elif x.startswith('__') and x.endswith('__'):
            return (QLineEdit(''), x[2:-2])

        else:
            return L(x)

    elif isinstance(x, list) and isinstance(x[0], str):
        if len(x) == 1 or len(x) == 2:
            return B(*x)
        else:
            raise ValueError('Invalid syntax: ' + str(x))

    elif callable(x) and not isinstance(x, type) and hasattr(x, '__name__'):
        return _AutoConnectButton(x.__name__.replace('_', ' '), x)

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


def splash(text,
           textalign=Qt.AlignHCenter | Qt.AlignVCenter,
           width=None,
           height=None,
           color=Qt.lightGray,
           image=None):
    '''Display and return a splash screen.

    This function displays a splashscreen and returns a QSplashScreen instance.

    The splashscreen must be closed with close() or finish(gui.window()).
    Alternatively, it will close when the user clicks on it.
    '''
    if image is None:
        if width is None:
            width = 400
        if height is None:
            height = 100
        pixmap = QPixmap(width, height)
        pixmap.fill(color)
    else:
        pixmap = QPixmap(image)
    splash = QSplashScreen(pixmap)
    splash.showMessage(text, alignment=textalign)
    splash.show()
    app = QApplication.instance()
    app.processEvents()
    return splash


def connect(widget, signal_name='default', slot=None):

    if hasattr(widget, '_gui'):
        gui = widget._gui
    else:
        raise TypeError('Widget %s does not seem to belong to any '
                        'Gui object' % widget.__class__.__name__)

    if signal_name == 'default':
        try:
            signal_name = _default_signal_lookup(widget)
        except KeyError as e:
            raise ValueError('No default signal for widget %s ' %
                             str(widget.__class__)) from e
    try:
        signal = getattr(widget, signal_name)
    except AttributeError as e:
        raise ValueError('No signal %s found for widget %s' %
                         (signal_name, str(widget.__class__))) from e

    # Custom signal with default handler for get()
    if slot is None:
        slot = functools.partial(gui._event_handler, signal, widget)

    if _bound_method(slot, to_whom=gui):
        use_slot = slot
    else:
        use_slot = functools.partial(slot, gui)

    signal.connect(_exception_wrapper(use_slot, gui))


class Gui:
    '''Main GUI class.

    The GUI is defined passing to the initializer a set of QT widgets
    organized in rows of equal length. All other methods that expect
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
                               persistence=PERSISTENT,
                               title='',
                               font=None,
                               manage_threads=True,
                               setup=None,
                               use_formats=True):

        # This line must be the first one in this method otherwise
        # __setattr__ does not work.
        self.__dict__['_guietta_properties'] = {}

        self.userdata = SimpleNamespace()

        if persistence == self.PERSISTENT:
            _add_to_persistence_list(self)

        self._layout = QGridLayout()
        self._widgets = {}                # widgets by name
        self._counter = defaultdict(int)  # widgets counter
        self._original_names = {}         # Reverse widget name lookup
        self._window = None
        self._app = QApplication.instance()
        self._font = font

        self._manage_threads = manage_threads
        self._main_thread = threading.get_ident()

        self._timer = None
        self._timer_count = 0
        self._user_timer_callback = None

        self._get_handler = False   # These three for the get() method
        self._event_queue = queue.Queue()
        self._closed = False
        self._inverted = False
        self._exception_mode = exceptions
        self._create_properties = create_properties

        self.images_dir = images_dir
        self.is_running = False
        self.use_formats = use_formats

        # Predefined button groups
        self._groups = [QButtonGroup() for i in range(10)]

        # Setup function
        if setup and not callable(setup):
            raise Exception('Setup value must be callable')

        self._setup_func = setup
        self._setup_done = False
        self._subguis_to_setup = []

        # Input argument checks
        self._rows = Rows(lists)
        self._rows.map_in_place(_convert_compacts)
        self._rows.map_in_place(_create_default_widgets)
        self._rows.map_in_place(functools.partial(_create_deferred, self))
        self._rows.map_in_place(_collapse_names)
        self._rows.map_in_place(_check_widget)

        # Intermediate step that will be filled by replicating
        # widgets when ___ and III are encountered.
        step1 = self._rows.copy(init=None)

        # Expand the combined widgets
        for i, j, element in self._rows.enumerate(skip_specials=False):
            if isinstance(element, _CombinedWidget):
                element.place(self._rows, i, j)  # This modifies rows

        # Expand remaining ___ and 'III' replicating
        # the widgets from the previous column and row.
        for i, j, element in self._rows.enumerate(skip_specials=False):
            if element == _:
                element = None
            else:
                if element == ___:
                    if j > 0:
                        element = step1[i, j-1]
                    else:
                        raise IndexError('___ at the beginning of a row')
                if element == III:
                    if i > 0:
                        element = step1[i-1, j]
                    else:
                        raise IndexError('III at the start of a column')
                if element is None:
                    raise ValueError('Continuation from empty grid cell')

            step1[i, j] = element

        # Now a multi-cell widget has been replicated both in rows
        # and in columns. Look for repetitions to calculate spans.

        done = set([None])  # Skip empty elements
        for i, j, element in step1.enumerate():
            if element not in done:
                rowspan = 0
                colspan = 0
                for ii in range(i, len(lists)):
                    if step1[ii, j] == element:
                        rowspan += 1
                for jj in range(j, len(lists[0])):
                    if step1[i, jj] == element:
                        colspan += 1

                widget, name = self._get_widget_and_name(element)
                if hasattr(widget, '_gui'):
                    raise Exception("Widget %s already has a '_gui' attribute" % name)
                widget._gui = self
                ContextMixIn.convert_object(widget)
                self._layout.addWidget(widget, i, j, rowspan, colspan)
                self._widgets[name] = widget
                done.add(element)

        self._align_guietta_properties()
        self.title(title)

    def _setup(self):
        '''
        Call the setup function, if any, for this GUI and all
        sub-GUIs. Also enable stdout/err redirection before setting up.
        '''
        StdoutLog.active = True

        if not self._setup_done:
            if self._setup_func:
                _exception_wrapper(self._setup_func, self)(self)
            for subgui in self._subguis_to_setup:
                subgui._setup()

        self._setup_done = True

    def _align_guietta_properties(self):
        '''Make sure that any and all widgets have a property'''

        self._guietta_properties.clear()
        if not self._create_properties:
            return
        
        for name, widget in self._widgets.items():
            if hasattr(widget, '__guietta_property__'):
                prop = widget.__guietta_property__()
                if isinstance(prop, GuiettaProperty):
                    pass
                else:
                    try:
                        get, set = widget.__guietta_property__()
                        assert callable(get)
                        assert callable(set)
                    except (TypeError, AssertionError) as e:
                        errmsg = ('__guietta_property__() must return '
                                  'a tuple with two callables')
                        raise TypeError(errmsg) from e
                        
                    prop = GuiettaProperty(get, set, widget)
            else:
                prop = _guietta_property(widget)
            self._guietta_properties[name] = prop

    @property
    def widgets(self):
        '''Read-only property with the widgets dictionary'''
        return self._widgets

    @property
    def names(self):
        '''Read-only property with the normalized -> original mapping'''
        return self._original_names

    def proxy(self, name):
        '''Returns the *guietta property* for a (normalized) widget name.

        A guietta property is an instance of the *GuiettaProperty* class,
        with two attributes: get() and set()
        '''
        name = normalized(name)
        return self.__dict__['_guietta_properties'][name]

    def __getattr__(self, name):
        '''Use guietta_properties to emulate properties on this instance'''

        if name in self.__dict__['_guietta_properties']:
            return self.__dict__['_guietta_properties'][name].get()

        # Default behaviour
        raise AttributeError(name)

    def __setattr__(self, name, value):
        '''Use guietta_properties to emulate properties on this instance'''

        if name in self.__dict__['_guietta_properties']:
            self.__dict__['_guietta_properties'][name].set(value)
            return

        # Default behaviour
        super().__setattr__(name, value)

    def _get_widget_and_name(self, element):
        '''Fish out the widget and its name from a declaration.

        Several possibilities:
            - (widget, 'name')  - type checks should have already been
                                  performed before, hopefully
            - widget            - if widget defines text() or title(), use
                                  that as the name, otherwise
                                  use the class name

        - remove special characters, only leave a-zA-Z0-9
        - auto-number duplicate names.
        '''
        if isinstance(element, tuple):
            widget, original_name = element
        else:
            widget = element
            if hasattr(widget, 'text'):
                original_name = widget.text()
            elif hasattr(widget, 'title'):
                original_name = widget.title()
            else:
                original_name = widget.__class__.__name__

        name = normalized(original_name)

        # If the name is a duplicate, auto-number it starting with 2.
        self._counter[name] += 1
        if self._counter[name] > 1:
            name = name + str(self._counter[name])

        self._original_names[name] = original_name

        return widget, name

    def row_stretch(self, *lists):
        '''Defines the row stretches
        
        Arguments are lists as in the initializer. Since typically all
        rows have the same stretch, it is allowed to define just one or only
        a few rows in this method.

        Every element in the lists must be a number, that will be passed to the
        setRowStretch() QT function, or _ if no particular stretch is desired.
        '''        
        rows = Rows(lists)
        rows.check_same(self._rows, allow_less_rows=True)

        for i, _, stretch in rows.enumerate():
            self._layout.setRowStretch(i, stretch)

    def column_stretch(self, *lists):
        '''Defines the column stretches

        Arguments are lists as in the initializer. Since typically all
        rows have the same stretch, it is allowed to define just one or only
        a few rows in this method.

        Every element must be a number, that will be passed to the
        setColumnStretch() QT function, or _ if no particular stretch
        is desired.
        '''
        rows = Rows(lists)
        rows.check_same(self._rows, allow_less_rows=True)

        for _, j, stretch in rows.enumerate():
            self._layout.setColumnStretch(j, stretch)

    def events(self, *lists):
        '''Defines the GUI events.

        Arguments are lists as in the initializer. It is allowed to define
        just one or only a few rows in this method, if for example
        the last rows do not contain widgets with associated events.

        Every element is a tuple with:

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
        rows = Rows(lists)
        rows.check_same(self._rows, allow_less_rows=True)

        rows.map_in_place(_process_slots)

        for i, j, pair in rows.enumerate():
            item = self[i,j]
            signal_name, slot = pair
            connect(item, signal_name, slot)

    def fonts(self, *lists):
        '''Defines the fonts used for each GUI widget.

        Arguments are lists as in the initializer. It is allowed to define
        just one or only a few rows in this method, if for example
        the last rows do not contain widgets whose fonts need not
        to be modified.

        Every element is either a QFont instance, a string with a font
        family name (.e.g 'Helvetica'), or a tuple with the QFont
        constructor elements: family string, point size, weight, and italic,
        int that order. All except the family string are optional, point size
        and weight ar integers, and italic is a boolean True/False. All these
        specifications are valid:

            - QFont('helvetica', pointSize=12)
            - 'helvetica'
            - ('helvetica', 12, 1, True)

        Use _ for widgets that do not need their fonts to be changed.
        '''
        rows = Rows(lists)
        rows.check_same(self._rows, allow_less_rows=True)

        rows.map_in_place(_process_font)

        for i, j, font_spec in rows.enumerate():
            self[i,j].setFont(font_spec)

    def rename(self, *lists):
        '''Overrides the default widget names.

        Arguments are lists as in the initializer. It is allowed to define
        just one or only a few rows in this method, if for example
        the last rows do not contain widgets that must be renamed.

        Every element is a string with the new name
        for the widget in that position. Use _ for widgets that do not
        need to be renamed.
        '''
        rows = Rows(lists)
        rows.check_same(self._rows, allow_less_rows=True)

        rows.map_in_place(_check_string)

        names_by_widget = {v: k for k, v in self._widgets.items()}

        for i, j, new_name in rows.enumerate():
            widget = self[i,j]
            old_name = names_by_widget[widget]

            self._widgets[new_name] = self._widgets[old_name]
            del self._widgets[old_name]

        self._align_guietta_properties()

    def timer_start(self, callback, interval=1.0):
        '''Set up a timer to call *callback* every *interval* seconds.
        
        The callback will receive the Gui instance as its only argument.
        '''
        self._timer = QTimer()
        self._user_timer_callback = _exception_wrapper(callback, self)
        self._timer.timeout.connect(self._timer_callback)
        self._timer.start(interval*1000)

    def timer_stop(self):
        '''Stops the timer'''
        if self._timer is not None:
            self._timer.stop()

    def timer_count(self):
        '''Returns the number of times the timer has been fired'''
        return self._timer_count

    def _timer_callback(self):
        self._timer_count += 1
        if self._user_timer_callback is not None:
            self._user_timer_callback(self)

    def timer(self, interval):
        '''Decorator that starts a function using the GUI timer'''
        def decorator(func):
            self.timer_start(func, interval)
            return func
        return decorator
        
    def __getitem__(self, name):
        '''Widget by coordinates [row,col]'''
        return self._layout.itemAtPosition(name[0], name[1]).widget()

    def layout(self):
        '''Returns the GUI layout, containing all the widgets'''
        return self._layout

    def window(self):
        '''
        Returns the window containing the GUI (an instance of QWidget).
        If the window had not been built before, it will be now.
        '''
        if self._window is None:
            self._window = QWidget()
            self._window.setLayout(self._layout)
            self._window.closeEvent = self._close_handler
            if self._font is not None:
                self._window.setFont(self._font)
        return self._window

    def font(self):
        return self.window().font()

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
        self._setup()
        self.show()
        self.is_running = True
        self._app.exec_()
        self.is_running = False

    def show(self):
        '''Shows the GUI. This call is non-blocking'''
        self.window().show()

    def close(self, dummy=None):    # Default argument for clicked(bool)
        '''Closes the window'''
        if self._window:
            self._window.close()

    def _invert_dicts(self):
        if not self._inverted:
            self._names_by_widget = {v: k for k, v in self._widgets.items()}
            self._inverted = True

    def iter(self):
        '''Returns an interable for GUI events

        for name, event in gui.iter():
        '''
        return GuiIterator(self)

    def get(self, block=True, timeout=None):
        '''Runs the GUI in queue mode

        In queue mode, no callbacks are used. Instead, the user should call
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
                try:
                    signal_name = _default_signal_lookup(widget)
                    signal = getattr(widget, signal_name)
                    handler = functools.partial(self._event_handler,
                                                signal,
                                                widget)
                    signal.connect(handler)
                except KeyError:
                    # Lookup failed, skipping widget
                    pass

            self._get_handler = True

        self.window().closeEvent = self._stop_handler
        self._setup()
        self.show()
        self._closed = False

        if (block is False) or (timeout is not None):
            if (block is False) or (timeout < 0):
                timeout = 0
            QTimer.singleShot(timeout * 1000,
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

    def title(self, title):
        '''Sets the window title'''
        self.window().setWindowTitle(title)
        
    def execute_in_main_thread(self, f, *args):
        '''Make sure that f(args) is executed in the main GUI thread.

        If the caller is running a different thread, the call details
        are packaged into a QT event that is emitted. It will be eventually
        received by the main thread, which will execute the call.
        '''
        curr_thread = threading.get_ident()
        main_thread = self._main_thread

        if (curr_thread == main_thread) or (self._manage_threads is False):
            f(*args)
        else:
            app = QApplication.instance()
            app.postEvent(app, _result_event(QEvent.User, f, args))

    def execute_in_background(self, func, args=(), callback=None):
        '''
        Executes `func` in a background thread and updates GUI with a callback.

        When func is done, the callback is called in the GUI thread.
        The callback receives a reference to this Gui instance as the first
        argument, plus whatever was returned by `func` as additional
        arguments.
        '''
        if not callable(func):
            raise TypeError('func must be a callable')
        if callback is not None:
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
        '''
        Returns the selected items in widget *name*.
        Raises TypeError if the widget does not support selection.
        '''
        widget = self.widgets[name]

        if hasattr(widget, 'selectedItems'):
            return map(lambda x: x.text(), widget.selectedItems())

        elif hasattr(widget, 'selectedText'):
            return widget.selectedText()

        elif hasattr(widget, 'currentText') and hasattr(widget, 'currentData'):
            return widget.currentText(), widget.currentData()

        elif hasattr(widget, 'currentText'):
            return widget.currentText()

        else:
            raise TypeError('Widget %s has no selection methods' % widget)

    def auto(self, func):
        '''Auto-connection decorator.

        Analyzes a function and auto-connects the function
        as a slot for all widgets that are accessed in the function itself.
        '''
        source = inspect.getsource(func)
        tree = ast.parse(textwrap.dedent(source))

        analyzer = _Analyzer(decorator_name=Gui.auto.__name__)
        analyzer.visit(tree)

        for widget_name in analyzer.accessed_widgets:

            if widget_name in self.widgets:
                try:
                    widget = self.widgets[widget_name]
                    connect(widget, slot=func)

                except ValueError:
                    # No default signal defined
                    pass

        return func

    def add_as_subgui(self, subgui):
        '''
        Set *subgui* as a sub-gui of this one. Exception modes will be
        propagated, and the sub-gui setup function will be called
        just after the main gui one.
        '''
        subgui._exception_mode = self._exception_mode
        self._subguis_to_setup.append(subgui)


class GuiIterator():
    '''An iterator that allows looping over the GUI events:

    for name, event in gui.iter():
        pass

    Iteration will stop when the GUI is closed.
    '''
    def __init__(self, gui):
        self.gui = gui

    def __iter__(self):
        return self

    def __next__(self):
        name, event = self.gui.get()
        if name is not None:
            return (name, event)
        else:
            raise StopIteration
         

# ___oOo___
