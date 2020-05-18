# -*- coding: utf-8 -*-

import unittest
from guietta.guietta import _process_slots, _specials

from PySide2.QtWidgets import QWidget

'''
    A callable is transformed into ('default', callable). The callable
    may be None to set it to the default get() handler.
    Tuples already in that format are type-checked.
    Specials (_, ___, III) are untouched.
    Other things raise a ValueError.
    '''


class ProcessSlotsTest(unittest.TestCase):

    def random_things(self):

        things = [1, 3.1415, QWidget(), None, ['a', 'list'],
                  {'a': 'dict'}, ('a', 'long', 'tuple')]

        for thing in things:
            with self.assertRaises(ValueError):
                _process_slots(thing)

    def test_specials(self):
        for x in _specials:
            assert _process_slots(x) is x

    def test_callable(self):
        x = min
        assert _process_slots(x) == ('default', min)

    def test_complete_slot(self):
        x = ('signalname', min)
        assert _process_slots(x) == ('signalname', min)

    def test_slot_with_None(self):
        x = ('signalname', None)
        assert _process_slots(x) == ('signalname', None)
