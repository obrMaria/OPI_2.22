#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import ind_test


studTestSuite = unittest.TestSuite()
studTestSuite.addTest(unittest.makeSuite(ind_test.StudTest))

runner = unittest.TextTestRunner(verbosity=2)
runner.run(studTestSuite)
