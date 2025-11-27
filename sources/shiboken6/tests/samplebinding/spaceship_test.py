#!/usr/bin/env python
# Copyright (C) 2025 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only WITH Qt-GPL-exception-1.0
from __future__ import annotations

'''Test cases for C++ 20 spaceship operators.'''

import os
import sys
import unittest

from pathlib import Path
sys.path.append(os.fspath(Path(__file__).resolve().parents[1]))
from shiboken_paths import init_paths
init_paths()

from sample import (FreeSpaceshipComparisonTester, SpaceshipComparisonTester,
                    NonEqualityComparisonTester)


class SpaceshipTest(unittest.TestCase):

    @unittest.skipUnless(SpaceshipComparisonTester.Enabled.HasSpaceshipOperator, "< C++ 20")
    def testSpaceshipOperator(self):
        t1 = SpaceshipComparisonTester(42)
        t2 = SpaceshipComparisonTester(42)
        self.assertEqual(t1, t2)
        self.assertTrue(t1 <= t2)
        self.assertTrue(t1 >= t2)
        t2 = SpaceshipComparisonTester(43)
        self.assertTrue(t1 < t2)
        self.assertFalse(t1 > t2)

    @unittest.skipUnless(SpaceshipComparisonTester.Enabled.HasSpaceshipOperator, "< C++ 20")
    def testNonHomogeneousSpaceshipOperator(self):
        t = SpaceshipComparisonTester(42)
        self.assertTrue(t < 43)
        self.assertTrue(t > 41)

    @unittest.skipUnless(SpaceshipComparisonTester.Enabled.HasSpaceshipOperator, "< C++ 20")
    def testFreeSpaceshipOperator(self):
        """Test a free operator<=>(). It does not provide equality
           as it is not defaulted."""
        t1 = FreeSpaceshipComparisonTester(1)
        t2 = FreeSpaceshipComparisonTester(2)
        self.assertTrue(t1 < t2)
        self.assertFalse(t1 > t2)

    @unittest.skipUnless(SpaceshipComparisonTester.Enabled.HasSpaceshipOperator, "< C++ 20")
    def testNonEqualSynthetization(self):
        ne_a = NonEqualityComparisonTester(1)
        ne_b = NonEqualityComparisonTester(1)
        self.assertTrue(ne_a == ne_b)
        # Verify that different instances with same value are not reported as "not equal",
        # (fooling the FallbackRichCompare() function which is generated for missing operators).
        self.assertFalse(ne_a != ne_b)


if __name__ == '__main__':
    unittest.main()
