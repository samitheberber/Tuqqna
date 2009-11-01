#!/usr/bin/env python

"""\
This module contains game interface for cli ui.
"""


from tuqqna.core.game import Game
from tuqqna.core.errors.board import NoMoreSlotsInColumn
from tuqqna.core.errors.game import Player1Wins
from tuqqna.core.errors.game import Player2Wins
from tuqqna.core.errors.game import GameHasBeenEnded
from tuqqna.core.errors.game import AtFirstStartNewGame


class CliUIGame(object):
    """\
Game interface for cli ui.

Method names are enough describing.
"""

    def __init__(self):
        self._game = Game()
        self._coinPosition = None
        self._message = "Game started."

    def addPlayer(self, name):
        self._game.addPlayer(name)
        self._message = "Added %s." % name

    def getPlayers(self):
        return [p.getName() for p in self._game.getPlayers()]

    def getPlayer1(self):
        player = self._game.getPlayer(1)
        if player:
            return player.getName()
        else:
            return "(none)"

    def getPlayer2(self):
        player = self._game.getPlayer(2)
        if player:
            return player.getName()
        else:
            return "(none)"

    def hasPlayers(self):
        return self._game.getPlayer(1) and self._game.getPlayer(2)

    def setBoard(self, width, height):
        self._game.setBoard(width, height)
        self._message = "Set board to %ix%i." % (width, height)
        self._game.newGame()
        self._coinPosition = None

    def boardWidth(self):
        return self._game.getWidth()

    def boardHeight(self):
        return self._game.getHeight()

    def player1(self, name):
        if not name in self.getPlayers():
            self._message = "Not found %s." % name
        else:
            self._game.changePlayer(1, self.getPlayers().index(name))
            self._message = "Selected %s to player 1." % name

    def player2(self, name):
        if not name in self.getPlayers():
            self._message = "Not found %s." % name
        else:
            self._game.changePlayer(2, self.getPlayers().index(name))
            self._message = "Selected %s to player 2." % name

    def isStarted(self):
        if self._game.isStarted():
            self._message = "Game is started."
            return True
        else:
            return False

    def coinPosition(self):
        msg = self._message
        if self.isStarted() and self._coinPosition == None:
            self._coinPosition = int(self.boardWidth() / 2)
        self._message = msg
        return self._coinPosition

    def moveCoinLeft(self):
        if not self.isStarted():
            return
        position = self.coinPosition()-1
        if position >= 0:
            self._coinPosition = position
            self._message = ""
        else:
            self._message = "Can't move more to left."

    def moveCoinRight(self):
        if not self.isStarted():
            return
        position = self.coinPosition()+1
        if position < self.boardWidth():
            self._coinPosition = position
            self._message = ""
        else:
            self._message = "Can't move more to right."

    def dropCoin(self):
        msg = self._message
        if not self.isStarted():
            return
        self._message = msg
        try:
            self._game.drop(self.coinPosition())
            self._message = ""
        except Player1Wins:
            self._message = "Winner is %s." % self._game.getPlayer(1)
            raise Player1Wins
        except Player2Wins:
            self._message = "Winner is %s." % self._game.getPlayer(2)
            raise Player2Wins
        except GameHasBeenEnded:
            self._message = "Game ends draw."
            raise GameHasBeenEnded

    def coinLanded(self):
        return self._game.getLast()

    def latestMessage(self):
        return str(self._message)
