# -*- coding: utf-8 -*-

import unittest
from guietta.guietta import Gui, _

from PySide2.QtWidgets import QWidget


class InitTest(unittest.TestCase):

    def test_widget_autocounter(self):

        a1 = (QWidget(), 'foo')
        a2 = (QWidget(), 'foo')
        a3 = (QWidget(), 'foo')
        b1 = (QWidget(), 'bar')
        b2 = (QWidget(), 'bar')
        gui = Gui([a1, a2, a3], [b1, b2, _])

        assert len(gui.widgets) == 5

        names = ['foo', 'foo2', 'foo3', 'bar', 'bar2']
        for name in names:
            assert name in gui.widgets
