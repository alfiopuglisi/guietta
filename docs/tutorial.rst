
Tutorial
========

What you need
-------------

 - Python 3.5 or newer

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
The layout is specified with aa series of Python
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
encouranged to use spaces to make the GUI layout visible right in the code.

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
    
and to changee the *result* text::

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
regulary. Just for demonstration purpose, this loop re-uses the
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
should occupy most of the window. The followinge example introduces two
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
   - a widet can be continued vertically below with **III** 
     (the VS widget shown above)
   - the two continuations can be combined as shown for 'Big label'
     to obtain a big rectangular widget (here 'Big label' is a 3x3 widget).
     The widget must be in the top-left corner in the layout, while
     in the GUI it will appear centered.

The additional labels have been inserted to expand the layout. Without them,
QT would have compressed the empty rows and columns to nothing.


Events and callbacks
--------------------

Exception handling
------------------

Matplotlib
----------

 