#!/usr/bin/env python

"""\
Test Board tests all board relevant matters.
"""


import unittest

from tuqqna.core.board import Board
from tuqqna.core.player import Player
from tuqqna.core.errors.game import GameNotStartedError
from tuqqna.core.errors.board import NoMoreSlotsInBoard


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


class TestBoardPlayerAssign(unittest.TestCase):

    def setUp(self):
        self.board = Board(7, 6)

    def test_set_player1_for_board(self):
        player = Player("Player 1")
        self.board.setPlayer1(player)
        self.assertEquals(self.board.getPlayer1(), player)

    def test_set_invalid_player1_for_board(self):
        self.assertRaises(ValueError, self.board.setPlayer1, "Player 1")

    def test_set_player2_for_board(self):
        player = Player("Player 2")
        self.board.setPlayer2(player)
        self.assertEquals(self.board.getPlayer2(), player)

    def test_set_invalid_player2_for_board(self):
        self.assertRaises(ValueError, self.board.setPlayer2, "Player 2")


class TestBoardIsReady(unittest.TestCase):

    def setUp(self):
        self.board = Board(7, 6)

    def test_not_ready_when_no_players_is_set(self):
        self.assertRaises(GameNotStartedError, self.board.drop, 1)

    def test_not_ready_when_only_one_player_is_set_player1(self):
        self.board.setPlayer1(Player("Player 1"))
        self.assertRaises(GameNotStartedError, self.board.drop, 1)

    def test_not_ready_when_no_players_is_set_player2(self):
        self.board.setPlayer2(Player("Player 2"))
        self.assertRaises(GameNotStartedError, self.board.drop, 1)

    def test_is_ready_when_both_players_is_set(self):
        self.board.setPlayer1(Player("Player 1"))
        self.board.setPlayer2(Player("Player 2"))
        try:
            self.board.drop(1)
        except GameNotStartedError:
            self.fail("Game is now started")


class TestBoardOnButtonDrop(unittest.TestCase):

    def setUp(self):
        self.board = Board(7, 6)
        self.board.setPlayer1(Player("Player 1"))
        self.board.setPlayer2(Player("Player 1"))

    def test_droppoint_is_below_zero(self):
        self.assertRaises(ValueError, self.board.drop, -1)

    def test_droppoint_is_over_width(self):
        self.assertRaises(ValueError, self.board.drop, 8)

    def test_is_dropped_in_correct_column(self):
        self.board.drop(0)
        self.assertEquals(self.board.lastSlotWhereDropped(), 0)

    def test_no_last_dropped_before_first_drop(self):
        self.assertEquals(self.board.lastSlotWhereDropped(), None)


class TestBoardOnTurnOfPlayer(unittest.TestCase):

    def setUp(self):
        self.board = Board(7, 6)
        self.board.setPlayer1(Player("Player 1"))
        self.board.setPlayer2(Player("Player 2"))

    def test_player1_starts(self):
        self.assertEquals(self.board.playerInTurn(), self.board.getPlayer1())

    def test_player2_is_after_player1(self):
        self.board.drop(0)
        self.assertEquals(self.board.playerInTurn(), self.board.getPlayer2())

    def test_player1_is_after_player2(self):
        self.board.drop(0)
        self.board.drop(0)
        self.assertEquals(self.board.playerInTurn(), self.board.getPlayer1())


class TestBoardOnFillButtons(unittest.TestCase):

    def setUp(self):
        self.board = Board(7, 6)
        self.board.setPlayer1(Player("Player 1"))
        self.board.setPlayer2(Player("Player 2"))

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
        self.board.drop(0)
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
|X| | | | | | |
---------------
|O| | | | | | |
---------------
"""
        self.assertEquals(str(self.board), boardString)

    def test_drop_buttons_until_no_slots_in_column(self):
        self.board.drop(0)
        self.board.drop(0)
        self.board.drop(0)
        self.board.drop(0)
        self.board.drop(0)
        self.board.drop(0)
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
        self.board.drop(0)
        self.board.drop(0)
        self.board.drop(0)
        self.board.drop(0)
        self.board.drop(0)
        self.board.drop(0)
        self.assertRaises(NoMoreSlotsInBoard, self.board.drop, 0)

    def test_drop_buttons_in_every_column(self):
        self.board.drop(0)
        self.board.drop(1)
        self.board.drop(2)
        self.board.drop(3)
        self.board.drop(4)
        self.board.drop(5)
        self.board.drop(6)
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


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestBoardConstruction))
    suite.addTest(unittest.makeSuite(TestBoardPlayerAssign))
    suite.addTest(unittest.makeSuite(TestBoardIsReady))
    suite.addTest(unittest.makeSuite(TestBoardOnButtonDrop))
    suite.addTest(unittest.makeSuite(TestBoardOnTurnOfPlayer))
    suite.addTest(unittest.makeSuite(TestBoardOnFillButtons))
    return suite
