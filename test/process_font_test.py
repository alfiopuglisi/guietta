# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

import unittest
from guietta.guietta import _process_font, _

from PySide2.QtWidgets import QWidget
from PySide2.QtGui import QFont


class ProcessFontTest(unittest.TestCase):

    def test_underscore_is_not_changed(self):
        
        assert _process_font(_) is _

    def test_qfont_is_not_changed(self):
        
        f = QFont('Arial')
        assert _process_font(f) is f
        
    def test_wrong_input(self):

        things = [1, None, 3.1415, QWidget(), [1, 2, 3]]

        # Most things are not changed
        for thing in things:
            with self.assertRaises((ValueError, TypeError)):
                _ = _process_font(thing)

    def test_family_str(self):
        
        family = 'Arial'
        assert _process_font(family) == QFont('Arial')
        
    def test_tuple_partial_args(self):
        
        t = ('arial', 12, 3, True)
        
        for n in range(len(t)):
            assert _process_font(t[:n]) == QFont(*t[:n])
            
    def test_list_partial_args(self):
        
        lst = ['arial', 12, 3, True]
        
        for n in range(len(lst)):
            assert _process_font(lst[:n]) == QFont(*lst[:n])

