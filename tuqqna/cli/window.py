#!/usr/bin/env python


class CliUIWindow(object):

    def _getMaxX(self):
        return self._stdscr.getmaxyx()[1]

    def _getMaxY(self):
        return self._stdscr.getmaxyx()[0]
