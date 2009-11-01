#!/usr/bin/env python

"""\
Test Board tests all board relevant matters.
"""


import unittest

from tuqqna.core.board import Board
from tuqqna.core.player import Player
from tuqqna.core.errors.game import GameNotStartedError
from tuqqna.core.errors.game import GameHasBeenEnded
from tuqqna.core.errors.game import Player1Wins
from tuqqna.core.errors.game import Player2Wins
from tuqqna.core.errors.board import NoMoreSlotsInColumn


class BasicBoardTestCase(unittest.TestCase):

    def setUp(self):
        self.board = Board(7, 6)


class TestBoardConstruction(BasicBoardTestCase):

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


class TestBoardDropClass(BasicBoardTestCase):

    def _repeatDrop(self, times, drop):
        for i in xrange(times):
            self.board.drop(drop)

    def _repeatDrops(self, times, drop1, drop2):
        for i in xrange(times):
            self.board.drop(drop1)
            self.board.drop(drop2)


class TestBoardOnButtonDrop(TestBoardDropClass):

    def test_droppoint_is_below_zero(self):
        self.assertRaises(ValueError, self.board.drop, -1)

    def test_droppoint_is_over_width(self):
        self.assertRaises(ValueError, self.board.drop, 8)

    def test_is_dropped_in_correct_column(self):
        self.board.drop(0)
        self.assertEquals(self.board.lastSlotWhereDropped(), 0)

    def test_no_last_dropped_on_column_before_first_drop(self):
        self.assertEquals(self.board.lastSlotWhereDropped(), None)

    def test_is_dropped_in_correct_row(self):
        self.board.drop(0)
        self.assertEquals(self.board.lastRowtWhereLanded(), 5)

    def test_no_last_dropped_on_row_before_first_drop(self):
        self.assertEquals(self.board.lastRowtWhereLanded(), None)


class TestBoardOnTurnOfPlayer(TestBoardDropClass):

    def test_player1_starts(self):
        self.assertEquals(self.board.playerInTurn(), 1)

    def test_player2_is_after_player1(self):
        self.board.drop(0)
        self.assertEquals(self.board.playerInTurn(), 2)

    def test_player1_is_after_player2(self):
        self._repeatDrop(2, 0)
        self.assertEquals(self.board.playerInTurn(), 1)


class TestBoardOnFillButtons(TestBoardDropClass):

    def test_first_button_falls_on_bottom(self):
        self.board.drop(0)
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
|O| | | | | | |
---------------
"""
        self.assertEquals(str(self.board), boardString)

    def test_second_button_falls_on_top_of_first_one(self):
        self._repeatDrop(2, 0)
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
|X| | | | | | |
---------------
|O| | | | | | |
---------------
"""
        self.assertEquals(str(self.board), boardString)

    def test_drop_buttons_until_no_slots_in_column(self):
        self._repeatDrop(6, 0)
        boardString = """\
---------------
|X| | | | | | |
---------------
|O| | | | | | |
---------------
|X| | | | | | |
---------------
|O| | | | | | |
---------------
|X| | | | | | |
---------------
|O| | | | | | |
---------------
"""
        self.assertEquals(str(self.board), boardString)

    def test_drop_buttons_over_the_slots_in_column(self):
        self._repeatDrop(6, 0)
        self.assertRaises(NoMoreSlotsInColumn, self.board.drop, 0)

    def test_drop_buttons_in_every_column(self):
        for i in xrange(7):
            self.board.drop(i)
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
|O|X|O|X|O|X|O|
---------------
"""
        self.assertEquals(str(self.board), boardString)


class TestBoardEndConditions(TestBoardDropClass):

    def test_game_ends_draw(self):
        self._repeatDrops(3, 0, 1)
        self._repeatDrops(3, 2, 3)
        self._repeatDrops(3, 4, 5)
        self._repeatDrops(3, 6, 0)
        self._repeatDrops(3, 1, 2)
        self._repeatDrops(3, 3, 4)
        self._repeatDrops(2, 5, 6)
        self.board.drop(5)
        self.assertRaises(GameHasBeenEnded, self.board.drop, 6)

    def test_player1_wins(self):
        self._repeatDrops(3, 0, 1)
        self.assertRaises(Player1Wins, self.board.drop, 0)

    def test_player2_wins(self):
        self._repeatDrops(3, 0, 1)
        self.board.drop(2)
        self.assertRaises(Player2Wins, self.board.drop, 1)

    def test_player1_wins_horizontal(self):
        for i in xrange(3):
            self._repeatDrop(2, i)
        self.assertRaises(Player1Wins, self.board.drop, 3)

    def test_player1_wins_cross(self):
        self.board.drop(0)
        self.board.drop(1)
        self.board.drop(2)
        self.board.drop(3)
        self.board.drop(1)
        self.board.drop(2)
        self.board.drop(3)
        self.board.drop(3)
        self.board.drop(2)
        self.board.drop(1)
        self.assertRaises(Player1Wins, self.board.drop, 3)


def suite():
    suite = unittest.TestSuite()
    #suite.addTest(unittest.makeSuite(TestBoardConstruction))
    #suite.addTest(unittest.makeSuite(TestBoardOnButtonDrop))
    #suite.addTest(unittest.makeSuite(TestBoardOnTurnOfPlayer))
    #suite.addTest(unittest.makeSuite(TestBoardOnFillButtons))
    suite.addTest(unittest.makeSuite(TestBoardEndConditions))
    return suite
