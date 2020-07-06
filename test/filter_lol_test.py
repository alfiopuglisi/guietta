# -*- coding: utf-8 -*-

import unittest
from guietta.guietta import Rows


class MapRowsTest(unittest.TestCase):

    def test_map_rows(self):

        rows = Rows([[1, 3, 10], [3.14, 0, -2]])

        def func(x):
            return x * 2

        rows.map_in_place(func)

        assert rows[0,0] == 2
        assert rows[0,1] == 6
        assert rows[0,2] == 20
        assert rows[1,0] == 6.28
        assert rows[1,1] == 0
        assert rows[1,2] == -4
