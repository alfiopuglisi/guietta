# -*- coding: utf-8 -*-

import unittest
from collections import defaultdict
from guietta.guietta import _normalize


class NnormalizeTest(unittest.TestCase):

    def test_normalize(self):
        
        a = 'foobar'
        assert _normalize(a) == a
        
        a = 'FooBar_123'
        assert _normalize(a) == a

        a = 'Foo!Bar?-/4+`\ 123:*'
        assert _normalize(a) == 'FooBar4123'

