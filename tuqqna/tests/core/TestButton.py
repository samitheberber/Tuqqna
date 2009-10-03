#!/usr/bin/env python

"""\
Test Button tests all button relevant matters.
"""


import unittest

from tuqqna.core.button import Button


class TestButtonProperties(unittest.TestCase):

    pass


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestButtonProperties))
    return suite
