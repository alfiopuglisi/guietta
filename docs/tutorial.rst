
Tutorial
========

What you need
-------------

Python 3.5 or newer

Install Guietta
---------------

``pip install guietta``

This should also automatically install PySide2, if you don't already have it.
If you plan to use Matplotlib together with guietta, you should install that
too. It is not done automatically.

Should I learn QT before starting?
----------------------------------

No. Knowing QT will make it easier to digest the most advanced topics,
but there is no need for it.

Quickstart
----------

We will work with a simple assignment: make a GUI application that,
given a number, doubles it. Here is how we begin::

   from guietta import Gui, _
   
   gui = Gui( [ 'Enter number' , '__num__' , ['Go'] ],
              [ 'Result ---> ' , 'result'  ,   _    ] )
   gui.run()
   
This code is enough to display a GUI with three widgets. Let's see
what each line does.

   ``from Guietta import Gui, _``
   
Every GUI made with Guietta is an instance of the ``Gui`` class, so we
need to import it. We also use the special underscore **_**, explained later,
so we import it too.

::

    gui = Gui( [ 'Enter number' , '__num__' , ['Go'] ],
               [ 'Result ---> ' , 'result'  ,   _    ] )

Arguments to the ``Gui`` constructor define the GUI layout.
The layout is specified with a series of Python
`lists <https://docs.python.org/3/tutorial/introduction.html#lists>`_,
one for each widget row. Our example has two rows, so 
there are two lists. Each list element
must be a valid widget. Here we see four different ones:

  - ``'Enter number'``: a string will be converted to a simple text display
    (in GUI parlance it is called a *label*). It is possible to change
    the text later on.
  - ``'__num__'``: a string starting and ending with double underscores
    will be converted to an edit box (imagine a form to be filled out).
    The edit box is initially empty.
  - ``['Go']``: a string inside square brackets will be converted
    to a button that the user can click. The button's text can also be
    changed later if wanted.
  - ``_``: an underscore means no widget.

Notice how we formatted the lists to keep things aligned. You are
encouraged to use spaces to make the GUI layout visible right in the code.

The constructor will create all these widgets and arrange them
in a regular grid. At this point, the GUI is ready to be displayed.

   ``gui.run()``

This line displays the GUI and starts the QT event loop. This function
will not return until the GUI is closed (there are ways around this, and
we will see them later). If you try the GUI, you will notice that
the ``Go`` button does nothing, since we did not assign it any function.
We will see how to do that in the next chapters.


Guietta's magic properties
--------------------------

Each GUI widget is assigned a name, which is usually automatically
derived from the constructor: any text-based widget has a name that corresponds
to the initial widget text. Special characters in the text are removed
in order to be sure that the resulting name is a valid Python identifier.
In practice, this means that letters a-Z, A-Z, numbers 0-9 and underscores
are kept, preserving case, and everything else is removed, including spaces::

   gui = Gui(['This is button 2!'])
   
   gui.Thisisbutton2 = 'new text'

The GUI shown in the previous chapter will have five widgets: 
"Enternumber", "num", "Go", "Result", and "result". If a name is a duplicate,
it is auto-numbered starting with the number 2.

In case the widget name becomes too long, guietta supports a *tuple syntax*
to set a custom name::

   gui = Gui([ ('Very very long label text', 'short_name') ])

   gui.short_name = 'new text'

The tuple syntax can be used with any supported widget. The general form
is *(QWidget, 'name')*, where *QWidget* can be any of the supported
widget generation syntax (strings to create labels, etc.)

All widgets are available in the `widgets` dictionary, so it is possible
to use all ordinary QT methods::

  gui.widgets['result'].setText('foo')

but Guietta makes it much easier, by automatically creating *magic properties*
for the widgets::

  gui.result = 'foo'

Magic properties are not real Python properties, because they are not defined
in the class but instead are emulated using getattr/setattr, but behave
in the same way. Properties can be read too::

  labeltext = gui.Enternumber
  
Labels can be assigned anything::

  gui.result = 3.1415
  gui.result = ['a', 'b', 'c']
  gui.result = dict(a=1, b='bar', c=None)

A list will result in a multi-line label, one element per line. A dictionary
will be displayed using two columns, one item per line, with keys on the left
column and values on the right one. Anything else is converted to a string
using str() on the value being assigned.

Magic properties work for buttons and other widgets too, but with different
object types. For example,
a button will accept a callable that will be called when the button
is clicked. A complete list of property types is available in the
`reference guide <reference.html#properties>`_.

A special case where magic properties are also used are dynamical layouts,
described in more detail `here <#hierarchical-guis>`_.

Working with normalized names
+++++++++++++++++++++++++++++

It is possible to obtain the name corresponding to a certain text
using the *normalized()* module-level function::


    from guietta import normalized
    
    print(normalized('This is button 2!'))
    
this code will return 'thisisbutton2'.

It is also possible to recover the original text that was used to create
the widget, given the normalized name (this can be useful when using the
*get()* feature, described later, that returns the normalized name). The
*Gui.names* property is a mapping that provides the original name::

     gui.names['thisisbutton2']

would return 'This is button 2!'.

*normalized()* and *names* were added in version 0.4.

Define magic properties for custom widgets
++++++++++++++++++++++++++++++++++++++++++

Guietta's properties work on any widget that respects the following
protocol:

1. defines a *__guietta_property__()* method
#. that returns a tuple with two callables: *get()* and *set(value)*.

Note that get() and set() are just conventional names,
actual functions can have a different name. The get function must
take no arguments and return the value. The set function must
take exactly one positional value, and the return value (if any)
is ignored.

The following example shows a widget where the property is a
number shown as text::

    class MyLabel(QLabel):
        def __init__(self):
            super().___init__('0')

        def __guietta_property__(self):
            def get_number():
                return float(self.getText())
            def set_number(num):
                self.setText('%5.3f' % num)
                            
            return (get_number, set_number)

Property proxies
++++++++++++++++

If a widget is created with a text generated dynamically, it will not be
possible to use a magic property as described above::


    row = [ 'label%d'%x for x in range(10) ]
    gui = Gui(row)

if now we want to address all labels, we would need to explcitly write::

    gui.label0 = 'foo'
    gui.label1 = 'bar'
    ...
    
Guietta allows to retrieve a *proxy* for the widget properties. It is a
simple *namedtuple* of type *GuiettaProperty*, with two members: *get()*
and *set()*, the latter taking a single argument::

    p = gui.proxy('label0')
    p.set('foo')
    a = p.get()  # a is now 'foo'

which could be used as follows::

    for x in range(10):
       gui.proxy('label%d'%x).set('foo %d' % x)


Property proxies were introduced in version 0.4.

Property contexts
+++++++++++++++++

If you have tried to run the previous example from the command prompt,
you will have seen the following output when calling *set()*::

    ... 
    <guietta.guietta._returnUndoContextManager.<locals>.decorator.<locals>.wrapper.<locals>.InnerUndoContextManager object at 0x7f188487a5c0>
    ...

This is expected. The *set()* call can be used as a context manager to
temporarily replace the widget contents with something else. When the context
manager exists, the widget contents are automatically restored::

    gui.status = 'idle'
    label = gui.proxy('status')
    ...
    with label.set('busy'):
        ... do something
        
the label will show "busy" while the statements inside the *with* block are
executed, and will revert back to "idle" afterwards.

Property contexts were introduced in version 0.4.

GUI actions
-----------

There are several ways to assign actions. Most rely on QT concept of
*event*: an event is something that happens to a widget (for example,
a button is clicked), and this event causes some piece of code to be
executed. Events only work if the QT *event loop* has been started,
which is done automatically by *gui.run()*. The "GUI queues" chapter
later on describes how one can work without the event loop, if desired.

The events layer
++++++++++++++++

The canonical Guietta way to specify events is to add a *layer* to the gui,
using the *events()* method::


    gui = Gui( [ 'Enter number' , '__num__' , ['Go'] ],
               [ 'Result ---> ' , 'result'  ,   _    ] )
               
    gui.events([       _        ,     _     ,  recalc ],
               [       _        ,     _     ,   _     ] )


Notice how we have kept exactly the same layout for the Gui constructor
and the events() method. This makes immediately visible that the *recalc*
event has been assigned to the *Go* button, while other widgets are ignored.

An event assigned this way can be any Python callable,
thus we need to define a *recalc* function before the gui is constructed::

    def recalc(gui, *args):
        gui.result = float(gui.num)*2

The first argument to an event function is always the *gui* instance that
generated the event. Other arguments may be added depending on the QT signal
that generated the event. Since we are not interested in them, we put a
generic \*args there.

The recalc function is updating the Gui using the magic properties
described in the previous chapter. Since the properties always return strings,
it uses float() to convert the string to a number.

Custom events
*************

In QT, a single widget can have several different events. For example,
an edit box can trigger an event every single time the text is changed,
or just when Return is pressed. Guietta assigns to each widget a
*default event*, which is the one that makes sense most of the time
(the list of default events for each widget is listed in the
`reference guide <reference.html#signals>`_).

It is possible to specify a custom event using the tuple syntax::

    gui = Gui( [ 'Enter number' , '__num__' , ['Go'] ],
               [ 'Result ---> ' , 'result'  ,   _    ] )
               
    gui.events([       _  ,  ('textEdited', recalc) ,  recalc ],
               [       _  ,           _              ,   _     ] )

The tuple must be (*'event_name'*, *callable*). The event name must be a valid
one for the widget, and a list can be found in the QT documentation, where
it is called a *signal*. The QT documentation lists the possible
signals for each widget, `for example for edit boxes
<https://doc.qt.io/qt-5/qlineedit.html>`_, in the "Signals" chapter.

Here we are assigning the *recalc* function to the *textEdited* event,
which is fired every time the text in the editbox is updated by the user.
Try it and you should see the value in the result label updating
at every keystroke.

Assign a callable
+++++++++++++++++

Buttons (ordinary buttons, checkboxes and radio buttons, that in QT are
all derived from QAbstractButton) can be assigned any python callable using
Guietta's magic properties::

    def handler(gui, *args):
        print('handler!')
        
    gui.mybutton = handler

Due to how the QT signal/slots mechanism works, it is not possible to read
the same property to get the button handler.

Automatic events
++++++++++++++++

If your GUI events are relatively simple, you might be able to do away
with their definitions entirely, using the *gui.auto* decorator::

    @gui.auto
    def recalc(gui, *args):
            gui.result = float(gui.num)*2

    gui.run()

When the "auto" decorator is used, Guietta will inspect the function code,
detect any property read like the *gui.num* above (but not the
*gui.result*, which is a property store), and automatically connect
the decorated function to the default event of that widget. Since the default
event for editboxes is *returnPressed*, the above code will run every time
the user presses *Return* on the editbox. The *Go* button at this point
could be removed.

Notice that the *auto* decorator is a member of a *Gui* instance, and not
a standalone one. Thus any decorated function must be declared after
the gui is constructed.

.. note:: due to how the code introspection features work (from the 
          standard library
          `inspect <https://docs.python.org/3/library/inspect.html>`_
          module) the @auto decorator will not work on the
          Python command prompt.

The *with* statement
++++++++++++++++++++

We saved the best for last. Enter the *with* statement::

    with gui.Go:
       gui.result = float(gui.num)*2

    gui.run()

The "with *magic property*" statement will save the code block and execute
it when the corresponding widget, in this case the *Go* button, fires its
default event.

The *as* clause refers to the same widget, which is useful if the *with* block
needs to refer to the widget itself::

    with gui.widgetWithVeryLongName as w:
       gui.result = w.text()

Multiple *with* blocks can be defined, and multiple widgets can be
listed in a single with block, without limits::

    with gui.a, gui.b:
       gui.result = float(gui.a) + float(gui.b)


If multiple widgets are listed, the *as* clause, if present,
will refer to the last widget in the list.
       

While extremely simple and intuitive, this style has a number of caveats:

    - signal arguments are not supported. The example above was a mouse click,
      but for example a *valueChanged()* signal from a slider would not have
      transferred the new slider value.
    - nested *with* statements will not work
    - like the @auto decorator above, it is not guaranteed to work on
      a Python prompt. It works on the standard Python one, but for example
      will not work with some versions of IPython.
    - the code inside *with* block is also executed once when it is encoureted
      for the first time, before *gui.run()* is called.
      This is unavoidable due to how code is parsed by
      Python. Most probably, it will generate an exception (in this case,
      because the gui.num content cannot be converted to a float object),
      and the guietta's *with* code block will discard all such exceptions.

It is possible to protect such a code block using Guietta's is_running
attribute::

    with gui.Go:
       if gui.is_running:
           gui.result = float(gui.num)*2

this way, one is sure that the code will be executed only under *gui.run()*,
but most of the time there is no need.

Explicit connect
++++++++++++++++

Most of the above action assignments end up calling *guietta.connect()*,
which has the following signature::

    guietta.connect(widget, signal_name='default', slot=None)

It can be used to explicitly connect a certain *widget* instance
to the callable *slot*, when the signal *signal_name* is emitted.


Exception handling
++++++++++++++++++

You may have noticed that, in our events example above, there was
no exception catching in the event functions.
Guietta by default catches all exceptions and pops a warning up to the user
if one happens. This behavior can be modified with the
``guietta.Exceptions`` enum, which has four values:

   - Exceptions.POPUP: the default one, a warning popup is shown
   - Exceptions.PRINT: the exception is printed on standard output
   - Exceptions.SILENT: all exceptions are silently ignored
   - Exceptions.OFF: no exception is caught, you have to do all the work.

The value must be given to the Gui constructor using the ``exceptions``
keyword argument::

   from guietta import Gui, _, Exceptions

   gui = Gui( [ 'Enter number' , '__num__' , ['Go'] ],
              [ 'Result ---> ' , 'result'  ,   _    ],
              exceptions = Exceptions.SILENT )    # Ignore exceptions 

The ``exceptions`` keyword can also accept any Python callable. In this case,
when an exception occurs the callable will be called with the exception
as an argument.



GUI queues
++++++++++

A completely different way of getting events out of the guis is to use
Guietta's *get()* method instead of *run()*.

With *get()*, the GUI behaves like a
`queue <https://docs.python.org/3/library/queue.html>`_
of *events*. These events are exactly the same as the ones we have seen
before, but instead of triggering a function or a *with* block, they
are put into an internal queue.

*get()* blocks until an event happens. It returns the name of the widget
that generated the event, plus an *Event* object with additional information
about the event::

   name, event = gui.get()
   
By the way, *get()* automatically shows the GUI if had not been shown before.

If you try to call ``gui.get()`` and click on the *Go* button,
you should see something like this::

  >>> gui.get()
  ('Go', Event(signal=<bound PYQT_SIGNAL clicked of QPushButton object at 0x7fef88dc9708>, args=[False]))

here we see that the event name was Go, as expected, and the Event object
tells us some details about the QT signal. Most of the time, we do not
need to even look at the detailed information.

If instead you call ``gui.get()`` and click the X to close the window,
the result will be::

  >>> gui.get()
  (None, None)

This is how we discover that the user has closed the window.

 .. note:: if you have clicked multiple times on the *Go* button
           in between
           the *get()* calls, you will have to call ``gui.get()`` 
           the same number of times before getting ``(None, None)``,
           because you have to empty out the event queue.
           
The usual way of using *get()* is to put it into an infinite loop,
breaking out of it when we get None::

    while True:
        name, event = gui.get()
        
        if name == 'Go':
            print('You clicked Go!')
            gui.result = float(gui.num)*2
        
        elif name == None:
            break

It is important to keep whatever is done in the loop very short, because
for the whole time we are outside *get()*, the GUI is not responsive to
user clicks and will not be redrawn if dragged, etc.


A word on exceptions
********************

If you have tried the previous code clicking *Go* without entering
a number before, or entering something else like a letter, the loop
will have exited with an exception caused by the failed *float()* call.

This happens because, when using *get()*, the exception catching described
above is not used. Instead, we should be
prepared to catch any exception generated by the code. Rather than using
a big try/except for the whole loop, it is best to put the the exception
handling right where it is needed, in order to be able to display a
meaningful error message to the user. Something like this::

           if name == 'Go':
               try:
                   gui.result = float(gui.num)*2
               except ValueError as e:
                   gui.result = e

Notice how we are displaying the error message right in the GUI.

Non-blocking *get*
******************

The *get()* call shown before blocks forever, until an event arrives.
However the call syntax is identical to the standard library
`queue.get <https://docs.python.org/3/library/queue.html#queue.Queue.get>`_
call::

   Gui.get(self, block=True, timeout=None)

If we pass a *timeout* argument (in seconds), the call will raise a
``guietta.Empty`` exception if *timeout* seconds have passed without a event.
This feature is useful to "wake up" the event loop and perform some tasks
regularly. Just for demonstration purposes, this loop re-uses the
*Enter number* label to show a counter going up an 10 Hz. while still
being responsive to the *Go* button::

        from guietta import Empty

        counter = 0
        while True:
            try:
                name, event = gui.get(timeout=0.1)
            except Empty:
                counter += 1
                gui.Enternumber = counter
                continue
        
            if name == 'Go':
               try:
                   gui.result = float(gui.num)*2
               except ValueError as e:
                   gui.result = e
        
            elif name is None:
                break

Notice the ``continue`` statement in the except clause. If it was not there,
execution would have progressed to the ``if`` statement below, and the
handler for the *Go* button might be executed multiple times.

Using images
------------

Labels and buttons can display images instead of text: just write the
image filename as the label or button text, and if the file is found,
it will be used as an an image. By default, images are searched in the
current directory, but the *images_dir* keyword argument can be supplied
to the ``Gui`` constructor to change it. So for example::

    import os.path
    from guietta import Gui, _
    
    gui = Gui(
        
      [  _             , ['up.png']   , _              ],
      [  ['left.png']  ,     _        , ['right.png']  ],
      [  _             , ['down.png'] , _              ],
    
      images_dir = os.path.dirname(__file__))


This code will display four image buttons arranged in the four directions,
provided that you have four PNG images with the correct filename
in the same directory as the python script. Notice how we use ``os.path``
to get the directory where our script resides.

Radio buttons
-------------

Radio buttons can be created using the R() widget, which stands for a
QRadioButton() instance. By default, all radio buttons in a single Gui
instance are exclusive. If multiple radio buttons groups are desired, Guietta
makes available ten pre-defined widgets classes called R0, R1, R2 ... R9,
which will create radio buttons belonging to one of the 10 groups.
For example::

    from guietta import Gui, R1, R2, R3

    gui = Gui(
        [ R1('rad1')  ,  R2('rad3')  , R3('rad5')   ],
        [ R1('rad2')  ,  R2('rad4')  , R3('rad6')   ],
    )

    gui.run()

That code creates six radio buttons, belonging to three different
exclusive groups arranged vertically.

The `radio buttons example <https://github.com/alfiopuglisi/guietta/blob/master/guietta/examples/radio.py>`_ shows how
to connect radio buttons to events and how to check if a radio button
is checked or not.

Radio button text will be modified with the same rules for every other widgets,
see `Guietta's magic properties <tutorial.html#guietta-s-magic-properties>`_.

Pre-defined radio buttons were introduced in version 0.3.4.

Special layouts
---------------

Sometimes we would like for a widget to be bigger than the others,
spanning multiple rows or columns. For example a label with a long text,
or a horizontal or vertical slider, or again a plot made with Matplotlib
should occupy most of the window. The following example introduces two
new Guietta symbols, **___** (three underscores) and **III** (three
capital letter i) which are used for horizontal and vertical expansion::

    from guietta import Gui, _, ___, III, HS, VS
    
    gui = Gui(
        
      [ 'Big label' ,    ___    ,       ___       ,  VS('slider1') ],
      [     III     ,    III    ,       III       ,       III      ],
      [     III     ,    III    ,       III       ,       III      ],
      [      _      , 'a label' , 'another label' ,        _       ],
      [HS('slider2'),    ___    ,       ___       ,        _       ]
    )

We also introduce the new widgets ``HS`` (horizontal slider) and
``VS`` (vertical slider). The rules for expansion are:

   - a widget can be continued horizontally to the right with **___**
     (the HS widget shown above)
   - a widget can be continued vertically below with **III** 
     (the VS widget shown above)
   - the two continuations can be combined as shown for 'Big label'
     to obtain a big rectangular widget (here 'Big label' is a 3x3 widget).
     The widget must be in the top-left corner in the layout, while
     in the GUI it will appear centered.

The additional labels have been inserted to expand the layout. Without them,
QT would have compressed the empty rows and columns to nothing.


Matplotlib
----------

Matplotlib provides a QT-compatible widget. Guietta wraps it into its
M() widget::

    from guietta import Gui, M, ___, III, VS

    gui = Gui(
        
      [  M('plot') , ___ ,  ___ , VS('slider') ],
      [     III    , III ,  III ,     III      ],
      [     III    , III ,  III ,     III      ],
      [     III    , III ,  III ,  '^^^ Move the slider'  ],
     )

Here we define a big M widget, giving it the name *plot*. 
If a static plot was wanted, we could now directly draw into it. But
since we like flashy things, we will make a plot that updates based
on the slider position.

The M() widget has a magic property to refresh the plot: if you assign
it a numpy array, it will just replot itself. If the array is 2d, it will
use imshow(). Here is a simple callback to redraw the plot::

    import numpy as np
    
    def replot(gui, value):
        t = np.linspace(0, 1+value/10, 500)
        gui.plot = np.tan(t)

The callback, as usual, has the gui as its first argument. Since we intend
to connect it to the slider, it also has a *value* argument, that will be
the slider position. Guietta's sliders are basic QT sliders with a value
that can go from 0 to 99 included.

If more control is needed, one could manually draw onto the widget::

    import numpy as np
    
    def replot(gui, value):
    
        ax = gui.plot.ax
        ax.clear()
        ax.set_title('y=tan(x)')
        t = np.linspace(0, 1+value/10, 500)
        ax.plot(t, np.tan(t), ".-")
        ax.figure.canvas.draw()


The callback can find the axis to draw on using "gui.<widgetname>.ax".
It then proceeds to clear the axis and use normal Matplotlib commands.
At the end, the canvas is redrawn.

.. Note:: it is important to clear the axis before starting, otherwise
          the old plots will still be there and, in addition to confuse
          the drawing, things will slow down a lot very quickly because
          Matplotlib will be still redrawing all of them.

To simplify these requirements, Guietta provides a
`context manager <https://docs.python.org/3/library/stdtypes.html#typecontextmanager>`_
that handles the clearing and redrawing. Thus the above callback
can be simplified to this::

    from guietta import Ax
    
    def replot(gui, value):
    
        with Ax(gui.plot) as ax:
            ax.set_title('y=tan(x)')
            t = np.linspace(0, 1+value/10, 500)
            ax.plot(t, np.tan(t), ".-")

We now need to connect this callback to our slider::

    gui.events(
        
        [  _            ,  _ , _ ,   replot     ], 
        [  _            ,  _ , _ ,   _          ], 
        [  _            ,  _ , _ ,   _          ], )
    
and run the GUI::

    replot(gui, 1)
    gui.run()

Notice how we first call the callback ourselves, giving it a default
value, in order to have a plot ready when the GUI is displayed.

Multiple plots
++++++++++++++

The M() widget has an optional *subplots* keyword::

    M('myplot', subplots=(2,3))

this will create a widget with 6 subplots organized in two rows.
The *guietta.myplot.ax* member will be the return value from the
subplots call, so it will be two lists with three ax objects each.

.. Note:: if the subplots keyword is set to any value different
          from its default, the Ax context manager cannot be used.


Pyqtgraph
---------

*pyqtgraph* is a plotting module with less features than matplotlib, but
much faster. It is ideal if the graph must be updated frequently. Guietta
wraps it into its *PG()* widget::

    import numpy as np
    from guietta import Gui, PG, ___, III, _, VS
    
    gui = Gui(
      [  PG('myplot'),  ___, ___, VS('slider') ],
      [     III     , III, III,     III      ],
      [     III     , III, III,     III      ],
      [     III     , III, III,  '^^^ Move the slider'  ],
     )

Replotting in pyqtgraph is much simpler than in matplotlib: we just have
to call the widget's *plot()* method, setting *clear=True* to ensure that
the previous plot is erased::

    with gui.slider:
        t = np.linspace(0, 1+gui.slider/10, 500)
        gui.myplot.plot(t, np.tan(t), clear=True)

Now we initialize the plot with a default one, and run the gui::

    gui.slider = 1
    gui.run()

It is also possible to use the PG widget's magic property, which accepts
1d numpy arrays::

    gui.myplot = np.arange(100)

If something more complex is needed, remember that pyqtgraph are full-featured
QT widgets, so they can be instantiated and dropped into Guietta without
the need to use the PG() wrapper.

.. note: minimum version for pyqtgraph is 0.11.0. This is the first version
         to support PySide2, used by Guietta.

Support for pyqtgraph was introducted in version 0.3.5.

Images
++++++

For displaying images, the *PGI()* widgets provides a *pyqtgraph.ImageView*
widget. 2d numpy arrays can be assigned to its property::

   gui = Gui([PGI('myimage')])
   gui.myimage = np.arange(100).reshape((10,10))

Support for pyqtgraph images was introducted in version 0.3.9.


Splash screens
--------------

Guietta supports extremely basic splash screens, with the `guietta.splash`
function:

.. autofunction:: guietta.splash

The splash function was introducted in version 0.3.1.

Background processing
---------------------

Sometimes a handler function needs to run for a long time, and during
that time the GUI would be frozen. In order to avoid this, the Gui class
allows to span a function into a background thread. Once the function
is done, an optional callback in the main thread will be triggered.

.. autofunction:: guietta.Gui.execute_in_background

Using other QT classes
----------------------

Guietta makes available several other useful QT classes (like *QFileDialog*)
without the need to import directly from PySide2::

    from guietta import QFileDialog
    
a complete list is available in the
`reference guide <reference.html#qt-symbols-in-guietta>`_.

Hierarchical GUIs
-----------------

Sometimes you want to insert a Gui inside another one, for example
in a program that builds its interface dynamically from basic GUI building
blocks. Guietta supports it as a special case of its magic properties::

   gui.label = another_gui
   
if `gui` and `another_gui` are two guietta.Gui instances, the *gui.label*
widget (which could be any kind of widget) will be removed, and in its place
the entire *another_gui* layout will appear, complete with all its widgets

The `sub_layout example <https://github.com/alfiopuglisi/guietta/blob/master/guietta/examples/sub_layout.py>`_
shows this trick in action.

Groupboxes
++++++++++

Sub-layouts are commonly associated with group boxes, that draw a rectangle
with a title around a window section. Guietta supports the QGroupBox widget
with its *G* widget, which can be assigned directly another Gui instance::

    gui = Gui( [ G('my group') ] )

    gui.mygroup = another_gui

Instead of replacing the whole widget, this code will show the
child Gui instance inside the group box, keeping it visible.

See also the `groupbox example <https://github.com/alfiopuglisi/guietta/blob/master/guietta/examples/groupbox.py>`_

Packaging your application
-----------------------------

Guietta runs perfectly fine if you have a Python interpreter, but sometimes
you want to package a self-contained program which is able to run without
dependencies. Guietta does not provide anything specific, but there are
several programs that can do this for generic Python applications. One
such program is
`PyInstaller <https://doc.qt.io/qtforpython/deployment-pyinstaller.html>`_.

Please note that PyInstaller is an independent project and we cannot
give any guarantee that it will work, nor provide any support.



Next topic: the `reference guide <reference.html>`_.
