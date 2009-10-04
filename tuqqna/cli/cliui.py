#!/usr/bin/env python

import curses


class CliUI(object):

    pass


def start():
    stdscr = curses.initscr()
    while True:
        c = stdscr.getch()
        if c == ord('p'):
            PrintDocument()
        elif c == ord('q'):
            break  # Exit the while()
        elif c == curses.KEY_HOME:
            x = y = 0
    curses.endwin()
