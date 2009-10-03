#!/usr/bin/env python

"""\
Test Board tests all board relevant matters.
"""


import unittest

from tuqqna.core.board import Board


class TestBoardConstruction(unittest.TestCase):

    def setUp(self):
        self.board = Board(7, 6)

    def test_board_width(self):
        self.assertEquals(self.board.getWidth(), 7)

    def test_board_height(self):
        self.assertEquals(self.board.getHeight(), 6)

    def test_board_string_format(self):
        boardString = """\
---------------
| | | | | | | |
---------------
| | | | | | | |
---------------
| | | | | | | |
---------------
| | | | | | | |
---------------
| | | | | | | |
---------------
| | | | | | | |
---------------
"""
        self.assertEquals(str(self.board), boardString)



def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestBoardConstruction))
    return suite
