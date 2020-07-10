# Changelog

## [0.3.5] - 2020-07-10

### Added
  - title() method and construction keyword argument
  - pyqtgraph integration
  
### Changed
  - QComboBox default signal is now 'currentTextChanged' for better
    backward compatibility with older QT versions.

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
