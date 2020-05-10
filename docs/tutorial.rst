
Tutorial
========

What you need
-------------

Python 3.5 or newer

Install Guietta
---------------

``pip install guietta``

This should also automatically install PyQt5, if you don't already have it.
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
   gui.show()
   
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

   ``gui.show()``

This line displays the GUI. If you try it, you will notice that
the ``Go`` button does nothing, since we did not assign it any function.
We will see how to do that in the next chapters.

Reading GUIs
------------

For very simple GUIs like our one, we can use Guietta's *get()* method.
With *get()*, the GUI behaves like a
`queue <https://docs.python.org/3/library/queue.html>`_
of *events*. An event
is generated every time the user clicks on a button or presses *Return*
on an input box (later on we'll see a more comprehensive list of events.)

*get()* returns the event name, which is the same as the name of the
widget that generates it, plus an *Event* object with additional information
about the event::

   name, event = gui.get()
   
By the way, *get()* calls *show()* if the GUI had not been shown before,
so the ``gui.show()`` call can be skipped.

If you try to call ``gui.get()`` and click on the *Go* button,
you should see something like this::

  >>> gui.get()
  ('Go', Event(signal=<bound PYQT_SIGNAL clicked of QPushButton object at 0x7fef88dc9708>, args=[False]))

here we see that the event name was Test, as expected, and the Event object
tells us some details about the QT signal. Most of the time, we do not
need to even look at the detailed information.

If instead you call ``gui.get()`` and click the X to close the window,
the result will be::

  >>> gui.get()
  (None, None)

This is how we discover that the user has closed the window.

 .. Note:: if you have clicked multiple times on the *Go* button
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
        
        elif name == None:
            break

.. Note:: when comparing the event name with known string, remember
          that Guietta modified widget name to be a valid Python
          identifier: all "special" characters and spaces are removed,
          and only letters a-z, A-Z and numbers 0-9 are kept, together with
          underscores. So if your button is called *Go!*, the exclamation
          mark will be removed.

It is important to keep whatever is done in the loop very short, because
for the whole time we are outside *get()*, the GUI is not responsive to
user clicks.

Updating GUIs
--------------

Once the *Go* button has been clicked, we would like to update
the *result* text with the actual result. In order to make this very easy,
Guietta creates a
`property <https://docs.python.org/3/library/functions.html#property>`_
for each widget, using the widget name as the property name. Properties
can be read and assigned to. So to read the value from *__num__*
editbox you can do something like this::

    value = gui.num
    
and to change the *result* text::

    gui.result = 'some text'

The properties for labels and edit boxes returns strings when read,
and convert anything to strings using *str()* when set.    
Combining all this information, we can come up with a one-liner
to do our job::

    gui.result = float(gui.num)*2

here we use *float()* to convert the string returned by *gui.num* into
a number, while the conversion from the float result to the string
required by *result* will be done automatically. We simply put this
line into our loop::

    while True:
        name, event = gui.get()
        if name == 'Go':
            gui.result = float(gui.num)*2
        elif name == None:
            break

And the GUI will update the result every time the Go button is clicked.

A word on exceptions
++++++++++++++++++++

If you have tried the previous code clicking *Go* without entering
a number before, or entering something else like a letter, the loop
will have exited with an exception caused by the failed *float()* call.

This teaches us an important lesson: when using *get()*, we should be
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
Later on we will encounter more flexible ways to handle exceptions.

Non-blocking *get*
------------------

The *get()* call shown before blocks forever, until an event arrives.
However the call syntax is identical to the standard library
`queue.get <https://docs.python.org/3/library/queue.html#queue.Queue.get>`_
call::

   Gui.get(self, block=True, timeout=None)

If we can pass a *timeout* argument (in seconds), the call will raise a
``Gui.Empty`` exception if *timeout* seconds have passed without a event.
This feature is useful to "wake up" the event loop and perform some tasks
regularly. Just for demonstration purpose, this loop re-uses the
*Enter number* label to show a counter going up an 10 Hz. while still
being responsive to the *Go* button::

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
      [  ['left.png'] ,     _         , ['right.png']  ],
      [  _             , ['down.png'] , _           ,  ],
    
      images_dir = os.path.dirname(__file__))


This code will display four image buttons arranged in the four directions,
provided that you have four PNG images with the correct filename
in the same directory as the python script. Notice how we use ``os.path``
to get the directory where our script resides.

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

We also introduce new new widgets ``HS`` (horizontal slider) and
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


Callbacks
---------

If you have more than a few buttons, the manual event loop becomes
unwieldy. Most QT GUIs use callbacks, and Guietta can do it too.

In callback mode, our Python code stops while the QT event loop is running.
Every event triggers a specific function (called a *callback*) in the
Python code.
The callback does what it needs to do, and when it ends, the event loop
restarts. As in the *get()* case, it is important that callbacks execute
quickly, because the GUI does not respond to user while they are executing.

You can specify which callback is assigned to each widget after construction,
using the *gui.event()* method. Going back to our first example, here is
what we have to add::

    # Callback for the Go button
    def go(gui, dummy):
        gui.result = float(gui.num)*2
        
    gui.events( [  _            ,    _     , go  ],
                [  _            ,    _     ,  _  ] )
                
    gui.run()
            
The *events()* method takes as an input a series of lists with same
shape as the ``Gui`` constructor. The list elements are either **_** or
the Python function (or any callable) that has been assigned to the widget.

Note how we have kept the same layout as the constructor. This makes it
immediately visible that the *go* callback has been assigned to the *Go*
button.

The *gui.run* method will now show our GUI, and will also block until the
GUI is closed. Whenever the user click the *Go* button, the *go* method
will be executed. The *while* loop shown before can be removed completely.

All callbacks receive a reference to the current gui object as their
first argument. This makes it easy for them to read or set widget values.

In this example, the *go* callback has been assigned to the default
even for a button, which in QT is called *clicked(bool)*, and has an extra
argument used for checkbox buttons. Here it is not used, but we had to
provide an extra *dummy* argument to our callback.

Custom events
+++++++++++++

QT has a huge list of events. For example, an editbox can trigger an event
every time a key is pressed. These events can be added like this::

    gui.events( [  _            , ('textEdited', go) , go  ],
                [  _            ,       _            ,  _  ] )

A tuple (event name, function) will cause the function to be executed
as a callback for that event. In this case, the *go* callback will be executed
every single time the editbox text changes (and also when the *Go*
button is pressed). You have to know the event name,
which in QT is called a *signal*. The QT documentation lists the possible
signals for each widget, `for example for edit boxes
<https://doc.qt.io/qt-5/qlineedit.html>`_, in the "Signals" chapter.

Exception handling
++++++++++++++++++

You may have noticed that, in the callback example above, there was
no exception catching in the callback. This because, when using callbacks,
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

We need to define a callback to redraw the plot::

    import numpy as np
    
    def replot(gui, value):
    
        ax = gui.plot.ax
        ax.clear()
        ax.set_title('y=tan(x)')
        t = np.linspace(0, 1+value/10, 500)
        ax.plot(t, np.tan(t), ".-")
        ax.figure.canvas.draw()

The callback, as usual, has the gui as its first argument. Since we intend
to connect it to the slider, it also has a *value* argument, that will be
the slider position. Guietta's sliders are basic QT sliders with a value
that can go from 0 to 99 included.

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


