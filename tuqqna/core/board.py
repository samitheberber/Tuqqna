#!/usr/bin/env python

"""\
Game board module.
"""


class Board(object):

    def __init__(self, width, height):
        self._width = width
        self._height = height

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
