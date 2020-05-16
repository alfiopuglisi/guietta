# -*- coding: utf-8 -*-

import unittest
from collections import defaultdict
from guietta.guietta import _bound_method


class BoundMethodTest(unittest.TestCase):

    class A:
        def b(self):
            pass

    class B:
        def c(self):
            pass

    def d(foo):
        pass

    def test_bound_method(self):

        a = self.A()
        assert _bound_method(a.b, a) is True

    def test_bound_method_to_someone_else(self):

        a = self.A()
        b = self.B()
        assert _bound_method(a.b, b) is False

    def test_unbound_method(self):

        a = self.A()
        assert _bound_method(self.d, a) is False
