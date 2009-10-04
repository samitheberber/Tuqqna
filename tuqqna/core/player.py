#!/usr/bin/env python

"""\
Game player module.
"""


class Player(object):

    def __init__(self, name):
        self._name = name
        self._victories = 0
        self._defeats = 0

    def getName(self):
        return self._name

    def getVictories(self):
        return self._victories

    def wins(self):
        self._victories += 1

    def getDefeats(self):
        return self._defeats

    def defeats(self):
        self._defeats += 1

    def __str__(self):
        return self._name
