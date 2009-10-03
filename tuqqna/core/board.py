#!/usr/bin/env python

"""\
Game board module.
"""

from tuqqna.core.player import Player
from tuqqna.core.button import Button
from tuqqna.core.errors.game import GameNotStartedError
from tuqqna.core.errors.board import NoMoreSlotsInBoard


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
        if not isinstance(self._player1, Player)\
           or not isinstance(self._player2, Player):
            raise GameNotStartedError()
        elif slot < 0 or slot > self._width:
            raise ValueError
        self._lastSlot = slot
        button = Button(slot, self._getFirstEmptyRow(slot))
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

    def _getFirstEmptyRow(self, column):
        if len(self._player1Drops) == 0 and len(self._player2Drops) == 0:
            return self._height-1
        else:
            buttonsInSelectedColumn = map(lambda btn: btn.y() ,filter(
                lambda btn: btn.x() == column,
                self._player1Drops + self._player2Drops))

            if len(buttonsInSelectedColumn) == 0:
                return self._height-1
            else:
                buttonsInSelectedColumn.sort()
                firstEmpty = buttonsInSelectedColumn[0]-1
                if firstEmpty < 0:
                    raise NoMoreSlotsInBoard
                else:
                    return firstEmpty

    def __str__(self):
        buttonsInTuple = self._createButtonsInTuple()
        stringFormat = ""
        for i in xrange(self._width):
            stringFormat += "--"
        stringFormat += "-\n"
        for i in xrange(self._height):
            stringFormat += self._slotRowToString(filter(
                lambda (x, y, z): y == i
                , buttonsInTuple))
        return stringFormat

    def _slotRowToString(self, rowItems):
        string = ""
        for i in xrange(self._width):
            matches = map(lambda (x, y, z): z, filter(lambda (x, y, z): x == i, rowItems))
            if len(matches) == 0:
                string += "| "
            else:
                string += "|%s" % matches[0]
        string += "|\n"
        for i in xrange(self._width):
            string += "--"
        return string + "-\n"

    def _createButtonsInTuple(self):
        ready = []
        for i in self._player1Drops:
            ready.append((i.x(), i.y(), "O"))
        for i in self._player2Drops:
            ready.append((i.x(), i.y(), "X"))
        return ready
