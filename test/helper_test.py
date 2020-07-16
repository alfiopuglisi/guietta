# -*- coding: utf-8 -*-

import unittest
from guietta.guietta import _sequence, _mutable_sequence

from qtpy.QtWidgets import QWidget 

class HelperTest(unittest.TestCase):
    
    def test_sequence(self):

        ok_things = [ [1,2,3], ['a', 'b'], (1,2,3)]
        ko_things = [ None, 'foo', 3.1415, {'a': 'dict'}]
        
        for thing in ok_things:
            assert _sequence(thing) is True

        for thing in ko_things:
            assert _sequence(thing) is False

    def test_mutable_sequence(self):

        ok_things = [ [1,2,3], ['a', 'b'] ]
        ko_things = [ (1,2,3), None, 'foo', 3.1415, {'a': 'dict'}]
        
        for thing in ok_things:
            assert _mutable_sequence(thing) is True

        for thing in ko_things:
            assert _mutable_sequence(thing) is False
            
