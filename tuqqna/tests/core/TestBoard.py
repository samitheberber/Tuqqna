#!/usr/bin/env python

"""\
Test Board tests all board relevant matters.
"""


import unittest


class TestBoard(unittest.TestCase):

    pass


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestBoard))
    return suite
