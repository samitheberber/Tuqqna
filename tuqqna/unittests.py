#!/usr/bin/env python

import unittest
import tests

def getTestSuites():
    suite = unittest.TestSuite()
    for testsuite in tests.getTestSuites():
        suite.addTest(testsuite)
    return suite

if __name__ == "__main__":
    #unittest.main()
    unittest.TextTestRunner(verbosity=2).run(getTestSuites())
