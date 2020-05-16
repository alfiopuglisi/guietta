# -*- coding: utf-8 -*-

import unittest
from guietta.guietta import _filter_lol


class FilterLolTest(unittest.TestCase):

    def test_filter_lol(self):

        lol = [[1, 3, 10], [3.14, 0, -2]]

        def func(x):
            return x * 2

        _filter_lol(lol, func)

        assert lol == [[2, 6, 20], [6.28, 0, -4]]
