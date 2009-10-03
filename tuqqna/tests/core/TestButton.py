#!/usr/bin/env python

"""\
Test Button tests all button relevant matters.
"""


import unittest

from tuqqna.core.button import Button


class TestButtonCreation(unittest.TestCase):

    def test_create_one_button_with_some_cordinates(self):
        button = Button(0, 0)
        self.assert_(button.x() == 0 and button.y() == 0)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestButtonCreation))
    return suite

