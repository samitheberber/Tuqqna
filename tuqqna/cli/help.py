#!/usr/bin/env python

"""\
This module contains help window.
"""

from tuqqna.cli.window import CliUIWindow


class CliUIHelpWindow(CliUIWindow):
    """\
Help window.

Methods are enough describing.
"""

    def __init__(self, stdscr):
        self._stdscr = stdscr
        self._win = self._stdscr.subwin(3, self._getMaxX()-2, self._getMaxY()-4, 1)
        self._win.box()
        self._win.refresh()

    def setHelpText(self, text):
        if len(text) > self._getMaxX()-4:
            raise Error("Too small window.")
        self.clear()
        self._win.addstr(1, 1, text)
        self._win.refresh()

    def clear(self):
        self._win.clear()
        self._win.box()
        self._win.refresh()
