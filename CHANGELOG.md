# Changelog

## [0.3.1] - 2019-05-26

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

## [0.3.0] - 2019-05-18

### Changed
 - Using PySide2 bindings instead of PyQt5
