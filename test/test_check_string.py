# -*- coding: utf-8 -*-

import unittest
from guietta.guietta import _check_string, _specials

from PySide2.QtWidgets import QWidget


class CheckStringTestTest(unittest.TestCase):

    def test_string(self):

        strings = ['a', 'foo', 'bar']
        for x in strings:
            assert _check_string(x) is x

    def test_specials(self):

        for x in _specials:
            assert _check_string(x) is x

    def test_not_string(self):

        not_strings = [1, 3.1415, QWidget(), ['a', 'list'], ('a', 'tuple'),
                       {'a': 'dict'}, None]

        for x in not_strings:
            with self.assertRaises(TypeError):
                assert _check_string(x)
