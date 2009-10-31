#!/usr/bin/env python

"""\
Test Game engine tests all game engine relevant matters.
"""


import unittest

from tuqqna.core.game import Game
from tuqqna.core.player import Player
from tuqqna.core.errors.board import NoMoreSlotsInColumn
from tuqqna.core.errors.game import InvalidPlayerId
from tuqqna.core.errors.game import InvalidPlayerNumber
from tuqqna.core.errors.game import Player1Wins
from tuqqna.core.errors.game import Player2Wins
from tuqqna.core.errors.game import AtFirstStartNewGame
from tuqqna.core.errors.game import GameHasBeenEnded


class TestGameCreation(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    def test_get_game_string(self):
        self.assertEquals(str(self.game), "")

    def test_create_the_game_with_board(self):
        self.game.setBoard(7,6)
        self.assertEquals(self.game.getWidth(), 7)
        self.assertEquals(self.game.getHeight(), 6)
        self.assertEquals(str(self.game), "")

    def test_add_new_player_in_game(self):
        player = "Test player"
        self.game.addPlayer(player)
        self.assertTrue(player in map(lambda x: x.getName(), self.game.getPlayers()))

    def test_add_few_more_players_in_game(self):
        try:
            for i in xrange(4):
                player = "Player no. %i" % i
                self.game.addPlayer(player)
                if player in map(lambda x: x.getName(), self.game.getPlayers()):
                    continue
                else:
                    raise ValueError
        except ValueError:
            self.fail("Not every player added in game.")

    def test_set_player1(self):
        self.game.setBoard(7,6)
        testPlayer1 = "Test Player 1"
        self.game.addPlayer(testPlayer1)
        self.game.addPlayer("Test Player 2")
        self.game.addPlayer("Test Player 3")
        self.game.changePlayer(1, 0)
        self.assertEquals(self.game.getPlayer(1).getName(), testPlayer1)

    def test_set_player1_to_invalid_player(self):
        self.game.setBoard(7,6)
        self.game.addPlayer("Test Player 1")
        self.assertRaises(InvalidPlayerId, self.game.changePlayer, 1, 1)

    def test_set_player2(self):
        self.game.setBoard(7,6)
        testPlayer1 = "Test Player 1"
        self.game.addPlayer(testPlayer1)
        self.game.addPlayer("Test Player 2")
        self.game.addPlayer("Test Player 3")
        self.game.changePlayer(2, 0)
        self.assertEquals(self.game.getPlayer(2).getName(), testPlayer1)

    def test_set_player2_to_invalid_player(self):
        self.game.setBoard(7,6)
        self.game.addPlayer("Test Player 1")
        self.assertRaises(InvalidPlayerId, self.game.changePlayer, 2, 1)

    def test_set_invalid_player_number(self):
        self.game.setBoard(7,6)
        self.game.addPlayer("Test Player 1")
        self.assertRaises(InvalidPlayerNumber, self.game.changePlayer, 0, 0)

    def test_get_invalid_player_number(self):
        self.game.setBoard(7,6)
        self.assertRaises(InvalidPlayerNumber, self.game.getPlayer, 0)


class TestGameOnPlay(unittest.TestCase):

    def setUp(self):
        self.game = Game()
        self.game.setBoard(7,6)
        self.game.addPlayer("Test Player1")
        self.game.addPlayer("Test Player2")
        self.game.changePlayer(1, 0)
        self.game.changePlayer(2, 1)

    def test_game_is_started(self):
        self.assertTrue(self.game.isStarted())

    def test_game_is_started_string(self):
        gameString = """\
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
        self.assertEquals(str(self.game), gameString)

    def test_player1_drops_on_left(self):
        try:
            self.game.drop(0)
            gameString = """\
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
            self.assertEquals(str(self.game), gameString)
        except:
            self.fail("Error on first drop.")

    def test_player1_drops_on_left_coordinates(self):
        try:
            self.game.drop(0)
            self.assertEquals(self.game.getLast(), (0, 5))
        except:
            self.fail("Error on first drop.")

    def test_players_drop_on_left_to_full(self):
        try:
            for i in xrange(6):
                self.game.drop(0)
            gameString = """\
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
            self.assertEquals(str(self.game), gameString)
        except:
            self.fail("Error on dropping.")

    def test_players_drop_on_left_to_full_coordinates(self):
        try:
            for i in xrange(6):
                self.game.drop(0)
            self.assertEquals(self.game.getLast(), (0, 0))
        except:
            self.fail("Error on dropping.")

    def test_players_drop_on_left_to_over_full(self):
        try:
            for i in xrange(7):
                self.game.drop(0)
            self.fail("Error on dropping.")
        except NoMoreSlotsInColumn:
            gameString = """\
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
            self.assertEquals(str(self.game), gameString)

    def test_player1_wins(self):
        try:
            for i in xrange(3):
                self.game.drop(0)
                self.game.drop(1)
            self.game.drop(0)
            self.fail("Error on player 1 winning.")
        except Player1Wins:
            gameString = """\
---------------
| | | | | | | |
---------------
| | | | | | | |
---------------
|O| | | | | | |
---------------
|O|X| | | | | |
---------------
|O|X| | | | | |
---------------
|O|X| | | | | |
---------------
"""
            self.assertEquals(str(self.game), gameString)

    def test_player2_wins(self):
        try:
            for i in xrange(3):
                self.game.drop(0)
                self.game.drop(1)
            self.game.drop(2)
            self.game.drop(1)
            self.fail("Error on player 2 winning.")
        except Player2Wins:
            gameString = """\
---------------
| | | | | | | |
---------------
| | | | | | | |
---------------
| |X| | | | | |
---------------
|O|X| | | | | |
---------------
|O|X| | | | | |
---------------
|O|X|O| | | | |
---------------
"""
            self.assertEquals(str(self.game), gameString)

    def test_game_end_draw(self):
        try:
            x = 0
            y = 1
            for i in xrange(3):
                for j in xrange(3):
                    self.game.drop(x)
                    self.game.drop(y)
                x += 2
                y += 2
            for i in xrange(3):
                self.game.drop(6)
                self.game.drop(0)
            x = 1
            y = 2
            for i in xrange(3):
                for j in xrange(3):
                    self.game.drop(x)
                    self.game.drop(y)
                x += 2
                y += 2
            self.fail("Failed to get correct error.")
        except GameHasBeenEnded:
            pass


class TestGamePlayerWinnings(unittest.TestCase):

    def setUp(self):
        self.game = Game()
        self.game.setBoard(7,6)
        self.game.addPlayer("Test Player1")
        self.game.addPlayer("Test Player2")
        self.game.addPlayer("Test Player3")

    def test_no_victories_at_start(self):
        for player in self.game.getPlayers():
            self.assertEquals(player.getVictories(), 0)
            self.assertEquals(player.getDefeats(), 0)

    def test_player1_has_one_victory_after_one_match(self):
        self.game.changePlayer(1, 0)
        self.game.changePlayer(2, 1)
        self.assertEquals(self.game.getPlayer(1).getVictories(), 0)
        try:
            for i in xrange(3):
                self.game.drop(0)
                self.game.drop(1)
            self.game.drop(0)
            self.fail("No winning :/")
        except Player1Wins:
            self.assertEquals(self.game.getPlayer(1).getVictories(), 1)
            self.assertEquals(self.game.getPlayer(2).getDefeats(), 1)

    def test_no_new_game_started(self):
        self.game.changePlayer(1, 0)
        self.game.changePlayer(2, 1)
        try:
            for i in xrange(3):
                self.game.drop(0)
                self.game.drop(1)
            self.game.drop(0)
            self.fail("No winning :/")
        except Player1Wins:
            self.assertRaises(AtFirstStartNewGame, self.game.drop, 0)

    def test_player1_has_two_victory_after_two_match(self):
        self.game.changePlayer(1, 0)
        self.game.changePlayer(2, 1)
        self.assertEquals(self.game.getPlayer(1).getVictories(), 0)
        self.assertEquals(self.game.getPlayer(2).getVictories(), 0)
        self.assertEquals(self.game.getPlayer(1).getDefeats(), 0)
        self.assertEquals(self.game.getPlayer(2).getDefeats(), 0)
        try:
            for i in xrange(3):
                self.game.drop(0)
                self.game.drop(1)
            self.game.drop(0)
            self.fail("No winning :/")
        except Player1Wins:
            self.assertEquals(self.game.getPlayer(1).getVictories(), 1)
            self.assertEquals(self.game.getPlayer(2).getVictories(), 0)
            self.assertEquals(self.game.getPlayer(1).getDefeats(), 0)
            self.assertEquals(self.game.getPlayer(2).getDefeats(), 1)
            self.game.newGame()
            try:
                for i in xrange(3):
                    self.game.drop(0)
                    self.game.drop(1)
                self.game.drop(0)
                self.fail("No winning :/")
            except Player1Wins:
                self.assertEquals(self.game.getPlayer(1).getVictories(), 2)
                self.assertEquals(self.game.getPlayer(2).getVictories(), 0)
                self.assertEquals(self.game.getPlayer(1).getDefeats(), 0)
                self.assertEquals(self.game.getPlayer(2).getDefeats(), 2)
            except Player2Wins:
                self.fail("Wrong Winner")
        except Player2Wins:
            self.fail("Wrong Winner")

    def test_player1_wins_once_and_player_two_wins_once(self):
        self.game.changePlayer(1, 0)
        self.game.changePlayer(2, 1)
        self.assertEquals(self.game.getPlayer(1).getVictories(), 0)
        self.assertEquals(self.game.getPlayer(2).getVictories(), 0)
        self.assertEquals(self.game.getPlayer(1).getDefeats(), 0)
        self.assertEquals(self.game.getPlayer(2).getDefeats(), 0)
        try:
            for i in xrange(3):
                self.game.drop(0)
                self.game.drop(1)
            self.game.drop(0)
            self.fail("No winning :/")
        except Player1Wins:
            self.assertEquals(self.game.getPlayer(1).getVictories(), 1)
            self.assertEquals(self.game.getPlayer(2).getVictories(), 0)
            self.assertEquals(self.game.getPlayer(1).getDefeats(), 0)
            self.assertEquals(self.game.getPlayer(2).getDefeats(), 1)
            self.game.newGame()
            try:
                for i in xrange(3):
                    self.game.drop(0)
                    self.game.drop(1)
                self.game.drop(2)
                self.game.drop(1)
                self.fail("No winning :/")
            except Player2Wins:
                self.assertEquals(self.game.getPlayer(1).getVictories(), 1)
                self.assertEquals(self.game.getPlayer(2).getVictories(), 1)
                self.assertEquals(self.game.getPlayer(1).getDefeats(), 1)
                self.assertEquals(self.game.getPlayer(2).getDefeats(), 1)
            except Player1Wins:
                self.fail("Wrong Winner")
        except Player2Wins:
            self.fail("Wrong Winner")


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestGameCreation))
    suite.addTest(unittest.makeSuite(TestGameOnPlay))
    suite.addTest(unittest.makeSuite(TestGamePlayerWinnings))
    return suite
