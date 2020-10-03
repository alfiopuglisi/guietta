# -*- coding: utf-8 -*-

import unittest
from guietta.guietta import normalize


class NormalizeTest(unittest.TestCase):

    def test_normal_chars(self):
        a = 'foobar'
        assert normalize(a) == a

    def test_normal_chars2(self):
        a = 'FooBar_123'
        assert normalize(a) == a

    def test_special_chars(self):
        a = 'Foo!Bar?-/4+`\\ 123:*'
        assert normalize(a) == 'FooBar4123'
