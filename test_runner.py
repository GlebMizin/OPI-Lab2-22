#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import bd_testing


calcTestSuite = unittest.TestSuite()
calcTestSuite.addTest(unittest.makeSuite(bd_testing.CalcBasicTests))
calcTestSuite.addTest(unittest.makeSuite(bd_testing.CalcExTests))

runner = unittest.TextTestRunner(verbosity=2)
runner.run(calcTestSuite)