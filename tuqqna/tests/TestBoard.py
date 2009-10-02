#!/usr/bin/env python

import unittest

class TestBoard(unittest.TestCase):
    pass

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestBoard))
    return suite
