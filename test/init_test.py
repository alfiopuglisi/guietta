# -*- coding: utf-8 -*-

import unittest
from guietta import Gui, _

from PyQt5.QtWidgets import QWidget 

class InitTest(unittest.TestCase):
    
    def test_that_only_lists_of_qt_widgets_are_accepted(self):

        things = [1, 'a', [1, 2], QWidget(), self, 3.1415, ('a', 'tuple')]        
        
        for thing in things:
            with self.assertRaises(ValueError):
                print(thing)
                a = Gui(thing)
            
        list_of_lists = [[QWidget(), QWidget()], [QWidget(), QWidget()]]
        a = Gui(*list_of_lists)    # Does not raise

        
    def test_widget_autocounter(self):
        
        a1 = (QWidget(), 'foo')
        a2 = (QWidget(), 'foo')
        a3 = (QWidget(), 'foo')
        b1 = (QWidget(), 'bar')
        b2 = (QWidget(), 'bar')
        gui = Gui( [a1, a2, a3], [b1, b2, _])
        
        assert len(gui.widgets) == 5
        
        names = ['foo', 'foo2', 'foo3', 'bar', 'bar2']
        for name in names:
            assert name in gui.widgets
