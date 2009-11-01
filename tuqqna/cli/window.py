#!/usr/bin/env python


class CliUIWindow(object):
    """\
This class tells, how to handle window size.
"""

    def _getMaxX(self):
        return self._stdscr.getmaxyx()[1]

    def _getMaxY(self):
        return self._stdscr.getmaxyx()[0]
