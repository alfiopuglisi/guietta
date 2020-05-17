# -*- coding: utf-8 -*-

import unittest
from guietta.guietta import _collapse_names

from PyQt5.QtWidgets import QWidget

'''((widget, name1), name2) -> (widget, name2), arbitrarily nested'''


class CollapseNamesTest(unittest.TestCase):

    def test_no_collapse(self):

        things = [1, None, 3.1415, QWidget(), [1, 2, 3]]

        # Most things are not changed
        for thing in things:
            assert _collapse_names(thing) is thing

    def test_single_tuple(self):
        a = ('xxx', 'name')
        assert _collapse_names(a) == a

    def test_one_level(self):
        a = (('xxx', 'name1'), 'name2')
        b = _collapse_names(a)
        assert b == ('xxx', 'name2')

    def test_two_levels(self):
        a = ((('xxx', 'name1'), 'name2'), 'name3')
        b = _collapse_names(a)
        assert b == ('xxx', 'name3')
