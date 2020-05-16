# -*- coding: utf-8 -*-

import unittest
from guietta import Gui

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

        

