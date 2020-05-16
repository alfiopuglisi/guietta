# -*- coding: utf-8 -*-

import unittest
from guietta.guietta import _convert_compacts, L, B

from PyQt5.QtWidgets import QWidget, QLineEdit

'''
    Converts:
        '__xxx___' to QLineEdit('xxx')
        'xxx'     to L('xxx')
        ['xxx']   to B('xxx')
        ['xxx', 'yyy']   to B('xxx', 'yyy')
'''

class CompactsTest(unittest.TestCase):

    def test_convert_compacts(self):

        things = [1, None, 3.1415, QWidget(), [1,2,3]]

        # Most things are not changed
        for thing in things:
            assert _convert_compacts(thing) is thing

        x = _convert_compacts('__foo__')
        assert isinstance(x, QLineEdit)
        assert x.text() == 'foo'

        x = _convert_compacts('foo')
        assert isinstance(x, L)
        assert x._text_or_filename == 'foo'

        x = _convert_compacts(['foo'])
        assert isinstance(x, B)
        assert x._text_or_filename == 'foo'

        x = _convert_compacts(['foo', 'bar'])
        assert isinstance(x, B)
        assert x._text_or_filename == 'foo'
        assert x._text == 'bar'
        
        # Recursion
        x = _convert_compacts(('__foo__', 'name'))
        assert isinstance(x[0], QLineEdit)
        assert x[0].text() == 'foo'
        assert x[1] == 'name'

        x = _convert_compacts(('foo', 'name'))
        assert isinstance(x[0], L)
        assert x[0]._text_or_filename == 'foo'
        assert x[1] == 'name'

        x = _convert_compacts((['foo'], 'name'))
        assert isinstance(x[0], B)
        assert x[0]._text_or_filename == 'foo'
        assert x[1] == 'name'

        x = _convert_compacts((['foo', 'bar'], 'name'))
        assert isinstance(x[0], B)
        assert x[0]._text_or_filename == 'foo'
        assert x[0]._text == 'bar'
        assert x[1] == 'name'
        