#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_jplhorizons
----------------------------------

Tests for `jplhorizons` module.
"""

import unittest
from jplhorizons import jplhorizons


class TestJplhorizons(unittest.TestCase):

    def setUp(self):
        pass

    def test_login(self):
        with jplhorizons.Telnet() as tn:
            tn.get_spacecraft_elements('juno')

    def test_nocraft(self):
        with jplhorizons.Telnet() as tn:
            self.assertRaises(jplhorizons.UnknownObject, tn.get_spacecraft_elements, 'garblygook')

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
