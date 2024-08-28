# Changelog

## [1.6.2] - 2024-08-28

### Changed
  - Accept non-integer time intervals
  - Timers are stopped when the window is closed

## [1.6.1] - 2023-09-08

### Changed
  - Fixed 'with' syntax bug on Python 3.11+

## [1.6.0] - 2023-03-26

### Added
  - Led class

## [1.5.0] - 2023-02-25

### Added
  - Widget groups to set/get multiple widgets using any Python iterable
  - ValueSlider editbox now has a name, allowing it to be referenced

### Changed
  - Removed debug output
  - Fixed bug preventing "execute_in_main_thread" decorator to work
    when "execute_in_background" is not used as well.

## [1.4.1] - 2022-07-26

### Added
  - keyword "projection" to matplotlib M() widget,
    passed internally to add_subplot.

## [1.4.0] - 2022-03-31

### Added
  - HeartBeat widget

## [1.3.0] - 2022-03-29

### Changed
  - Inverted import order of PyQt5 and PySide2,
    giving priority to PyQt5 to fix compatibility
    problems with matplotlib

## [1.2.0] - 2022-03-29

### Added
  - Matplotlib widgets expose all methods of their
    Axes and AxesImage children widgets.
  - Convenience function colorbar() for matplotlib widgets
 
## [1.1.0] - 2022-03-27

### Added
  - Matplotlib updatable widgets MA()

## [1.0.0] - 2021-12-06

### Added
  - New syntax for edit field initialization
  - New syntax for automatic buttons with a callable
  - Optional checked parameter for radio buttons
  - Setup function to be executed after GUI initialization
  - Labels can be initialized with % format strings

### Changed
  - Fixed bug with matplotlib colobars
  - Sub-GUIs now inherit the exception mode of the main GUI
  - StdoutLog widget only captures output after GUI
    has been initialized, in order to avoid error messages
    "disappearing" if they happen before the GUI is shown.

## [0.6.1] - 2020-11-22

### Added
  - timer_count()

### Changed
  - the timer callback now gets the gui as its first argument
  - fixed bug where matplotlib images were rescaled every time the Ax
    decorator was used, if a colorbar was been created.


## [0.6.0] - 2020-11-21

### Added
  - password input field
  - timer_start() and timer_stop()

## [0.5.0] - 2020-10-04

### Added
  - iterator protocol to loop through GUI events
  - thread management options


## [0.4.0] - 2020-10-03

### Changed
  - Refactored matlotlib and pyqtgraph code into separate files
  
### Added
  - PGI() widget for pyqtgraph images.
  - pyqtgraph widgets: added magic properties for plots and images.
  - property proxies with the proxy() method
  - "undo" context manager for properties
  - connect() now has a default signal name


## [0.3.8] - 2020-07-20

### Changed
  - Workaround for bugs in some version of the "inspect" module.


## [0.3.7] - 2020-07-20

### Changed
  - Compatibility with old Matplotlib versions (<2.1)


## [0.3.6] - 2020-07-20

### Added
  - support for group boxes
  - hierarchical layouts ("child" Gui instances) using property assignments
  - font() method and construction keyword argument
  - matplotlib widgets: added magic properties, subplots, arbitrary
    calls upon redrawing.
  
### Changed
  - callback in background processing is now optional
  - documentation on readthedocs is finally properly versioned


## [0.3.5] - 2020-07-10

### Added
  - title() method and construction keyword argument
  - pyqtgraph integration
  
### Changed
  - QComboBox default signal is now 'currentTextChanged' for better
    backward compatibility with older QT versions.
  - Fallback to import from PyQt5 instead of PySide2 if the latter fails.


## [0.3.4] - 2020-07-06

### Added
  - Pre-defined radio button groups
  - Progress bar widget
  - Added default signal 'valueChanged' for QDial and QScrollBar
  
### Changed
  - Fixed bug for images when using the full file path
  - Fixed small bugs in the examples
  - "with" context manager now can reference imports and functions
    defined outside it.


## [0.3.3] - 2020-06-18

### Changed
  - Support for older PySide versions (v5.9+)
  - Fixed bug in ValueSlider layout
  - Internal refactor adding the new Rows class.

### Added
  - 'clicked' signal for Matplotlib widgets


## [0.3.2] - 2020-05-26

### Changed
  - Fixing incompatibilites between GitHub's and PyPI's README format.


## [0.3.1] - 2020-05-26

### Added
 - Support for ComboBoxes (using QComboBox)
 - Splash Screen (using QSplashScreen)
 - @auto decorator syntax
 - "with" context manager syntax
 - removed all widget-generating functions, all widgets are now classes
 - widgets can be specified with just the class, a widget with a default name
   will be allocated.
 
### Changed
 - "dropped" signal for list boxes (QListBox) renamed to "drop"


## [0.3.0] - 2020-05-18

### Changed
 - Using PySide2 bindings instead of PyQt5
