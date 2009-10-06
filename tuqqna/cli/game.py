#!/usr/bin/env python

"""\
"""


from tuqqna.core.game import Game


class CliUIGame(object):

    def __init__(self):
        self._game = Game()

    def addPlayer(self, name):
        self._game.addPlayer(name)

    def getPlayers(self):
        return map(lambda player: player.getName(), self._game.getPlayers())

    def setBoard(self, width, height):
        self._game.setBoard(width, height)

    def boardWidth(self):
        return self._game.getWidth()

    def boardHeight(self):
        return self._game.getHeight()

    def player1(self, name):
        if not name in self.getPlayers():
            raise ValueError
        self._game.changePlayer(1, self.getPlayers().index(name))

    def player2(self, name):
        if not name in self.getPlayers():
            raise ValueError
        self._game.changePlayer(2, self.getPlayers().index(name))
