# -*- coding: utf-8 -*-

import unittest
from collections import defaultdict
from guietta.guietta import Rows, _, ___, III


class EnumerateRowsTest(unittest.TestCase):

    def test_enumerate_rows(self):

        rows = Rows([[1, 3, 10], [3.14, 0, -2]])

        counter = 0

        for i, j, element in rows.enumerate():
            assert rows[i][j] == element
            counter += 1

        assert counter == 6

    def test_skip_specials_default(self):

        rows = Rows([[1, _, 10], [___, 0, III]])

        counter = 0

        for i, j, element in rows.enumerate():
            assert element is not _
            assert element is not ___
            assert element is not III
            counter += 1

        assert counter == 3

    def test_skip_specials_false(self):

        rows = Rows([[1, _, 10], [___, 0, III]])

        result = {}
        for i in range(2):
            result[i] = {}

        for i, j, element in  rows.enumerate(skip_specials=False):
            result[i][j] = element

        assert result[0][1] is _
        assert result[1][0] is ___
        assert result[1][2] is III
