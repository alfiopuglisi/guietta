# -*- coding: utf-8 -*-

import unittest
from guietta.guietta import Rows, _check_widget

from PySide2.QtWidgets import QWidget


class RowsCheckTest(unittest.TestCase):

    def test_that_only_lists_of_qt_widgets_are_accepted(self):

        things = [1, 'a', [1, 2], QWidget(), self, 3.1415, ('a', 'tuple')]

        for thing in things:
            with self.assertRaises(TypeError):
                Rows.check(thing)

        rows = Rows([[QWidget(), QWidget()], [QWidget(), QWidget()]])
        rows.map_in_place(_check_widget)  # Does not raise

    def test_that_rows_with_one_elements_are_expanded(self):

        widgets = [QWidget()] * 5
        single1 = [QWidget()]
        single2 = [QWidget()]
        single3 = [QWidget()]

        Rows.check([widgets, single1])
        Rows.check([single2, widgets])
        Rows.check([widgets, single3, widgets])

        assert len(single1) == 5
        assert len(single2) == 5
        assert len(single3) == 5

    def test_that_rows_must_have_equal_length(self):

        row1 = [QWidget()] * 5
        row2 = [QWidget()] * 5
        row3 = [QWidget()] * 4
        row4 = [QWidget()] * 4

        with self.assertRaises(ValueError):
            Rows.check([row1, row2, row3])

        with self.assertRaises(ValueError):
            Rows.check([row3, row4, row1])

        Rows.check([row1, row2])   # Does not raise
        Rows.check([row3, row4])   # Does not raise