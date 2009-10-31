#!/usr/bin/env python

"""
This is main game file of Tuqqna.
"""


import sys
import getopt

from tuqqna.cli import cliui


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help", "cli"])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
    # process options
    for o, a in opts:
        if o in ("-h", "--help"):
            print __doc__
            sys.exit(0)
        elif o in ("--cli"):
            try:
                cliui.start()
            except KeyboardInterrupt:
                return
