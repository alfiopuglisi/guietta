
How Guietta works
=================


For the constructor aruguments:

- argument checks (*layer_check()*)
    1. Check that all elements are iterables, raise ValueError if not.
    #. Take the longest
    #. Expand single-elements ones to the longest using ___
    #. Check that all rows have the same length, raise ValueError if not.

- Compact syntax is expanded (*convert_compacts()*) 
    1. 'xxx' is converted to L('xxx')
    #. '__xxx__' is converted to (QLineEdit(''), 'xxx')
    #. '__xxx__:yyy' is converted to (QLineEdit('yyy'), 'xxx')
    #. ['xxx', 'yyy'] is converted to B('xxx', 'yyy'), with 'yyy' optional.
       Lists with 0 or >2 elements raise ValueError
    #. 2-tuples are recursed into in order to expand 
       the first element if needed

- Labels and buttons are created (*create_deferred()*)

   * Labels
      1. L('xxx') becomes (QLabel('xxx'), 'xxx')
      #. L('xxx.png') becomes (QLabel(QPixmap('xxx.png')), 'xxx')
   * Buttons
      1. B('xxx') becomes (QPushButton('xxx'), 'xxx')
      #. B('xxx.png', 'yyy' becomes (QPushButton(QIcon('xxx.png')), 'yyy')
   * Automatic buttons (Quit, Yes, No.. etc) are created and connected
   * Separators are created
   * 2-tuples are rercursed into in order to expand
     the first element if needed.
       
- Multiple names are collapsed (*collapse_names()*)
    - Things like (((widget, 'name1'), 'name2'), 'name3')
      become (widget, 'name3'). Nesting is flattened for an arbitrary depth.

- Type check (*check_widget()*). All resulting widgets must be one of two types:
    1. A QWidget instance, or
    2. a 2-tuple (QWidget, 'name')


Instance properties
-------------------

Widgets values can be get/set like a property::

   gui.label = 'text'
   value = gui.slider

These property-like attributes are created on the fly when the GUI is
built. We cannot use real properties, because these are class attributes
and they would be shared between instances. Instead, there is a
dictionary *self._guietta_properties* which contains a mapping from property
name to a pair of get/set functions (a namedtuple is used for the pair
in order to have nice methods names). These methods are set to the ones
appropriate for the widget type at construction time.

The *_guietta_properties* dict is used by __getattr__ and __setattr__ to
emulate the property behaviour. Since these methods would be used
to lookup *_guietta_properties* itself, this mapping must be created in the
__init__ method as its first instruction, and using self.__dict__ instead
of direct attribute access.

