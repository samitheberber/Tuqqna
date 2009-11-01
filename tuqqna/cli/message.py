#!/usr/bin/env python

"""\
This module contains game message window.
"""

import curses

from tuqqna.cli.window import CliUIWindow


class CliUIGameMsgWindow(CliUIWindow):
        """\
Game message window.

Methods are enough describing.
"""

    def __init__(self, stdscr):
        self._stdscr = stdscr
        windowWidth = self._getMaxX() - 2
        self._win = stdscr.subwin(1, windowWidth, 1, 1)

    def setMessage(self, msg):
        self._win.clear()
        self._win.addstr(0, 0, msg)
        self._win.refresh()

    def getStr(self):
        curses.echo()
        value = self._win.getstr()
        curses.noecho()
        return value

    def clear(self):
        self._win.clear()
        self._win.refresh()
