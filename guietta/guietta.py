# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QApplication, QLabel, QWidget
from PyQt5.QtWidgets import QPushButton, QRadioButton, QCheckBox
from PyQt5.QtWidgets import QLineEdit, QHBoxLayout, QVBoxLayout

# Make a reference to ourselves.

g = __import__(__name__)

# Widget shortcuts

B = QPushButton
E = QLineEdit
_ = QLabel
C = QCheckBox
R = QRadioButton

class Gui:
    '''Main GUI object'''
    
    # List of lists for the layers
    def __init__(self, *args):
        pass

    def events(self, *args):
        '''Defines the GUI events'''
        pass

    def names(self, *args):
        '''Overrides the default names'''
        pass

    def colors(self, *args):
        '''Defines the GUI events'''
        pass

    def groups(self, *args):
        '''Defines the GUI events'''
        pass

    def __getattr__(name):
        '''Returns one of the current widgets, or a future reference.'''
        pass

    def __getitem__(name):
        '''widget by coordinates [row,col]'''
        pass

    def all(group=''):
        '''replicates command on all widgets'''
        pass