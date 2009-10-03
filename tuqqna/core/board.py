#!/usr/bin/env python

"""\
Game board module.
"""

from tuqqna.core.player import Player
from tuqqna.core.button import Button
from tuqqna.core.errors.game import GameNotStartedError


class Board(object):

    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._player1 = None
        self._player2 = None
        self._player1Drops = []
        self._player2Drops = []
        self._lastSlot = None

    def getWidth(self):
        return self._width

    def getHeight(self):
        return self._height

    def __str__(self):
        stringFormat = ""
        for i in xrange(self._width):
            stringFormat += "--"
        stringFormat += "-\n"
        for i in xrange(self._height):
            stringFormat += self._slotRowToString()
        return stringFormat

    def _slotRowToString(self):
        str = ""
        for i in xrange(self._width):
            str += "| "
        str += "|\n"
        for i in xrange(self._width):
            str += "--"
        return str + "-\n"

    def setPlayer1(self, player):
        if not isinstance(player, Player):
            raise ValueError
        self._player1 = player

    def getPlayer1(self):
        return self._player1

    def setPlayer2(self, player):
        if not isinstance(player, Player):
            raise ValueError
        self._player2 = player

    def getPlayer2(self):
        return self._player2

    def drop(self, slot):
        if not isinstance(self._player1, Player) or not isinstance(self._player2, Player):
            raise GameNotStartedError()
        elif slot < 0 or slot > self._width:
            raise ValueError
        self._lastSlot = slot
        button = Button(0, 0)
        if self.playerInTurn() == self._player1:
            self._player1Drops.append(button)
        else:
            self._player2Drops.append(button)

    def lastSlotWhereDropped(self):
        return self._lastSlot

    def playerInTurn(self):
        if len(self._player1Drops) == len(self._player2Drops):
            return self._player1
        else:
            return self._player2
