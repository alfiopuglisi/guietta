# -*- coding: utf-8 -*-

import unittest
from guietta.guietta import _normalize


class NormalizeTest(unittest.TestCase):

    def test_normal_chars(self):
        a = 'foobar'
        assert _normalize(a) == a

    def test_normal_chars2(self):
        a = 'FooBar_123'
        assert _normalize(a) == a

    def test_special_chars(self):
        a = 'Foo!Bar?-/4+`\\ 123:*'
        assert _normalize(a) == 'FooBar4123'
