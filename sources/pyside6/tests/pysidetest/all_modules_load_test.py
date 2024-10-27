# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only WITH Qt-GPL-exception-1.0
from __future__ import annotations

import os
import sys
import unittest

from pathlib import Path
sys.path.append(os.fspath(Path(__file__).resolve().parents[1]))
from init_paths import init_test_paths
init_test_paths(False)

import PySide6


# Note:
# "from PySide6 import *" can only be used at module level.
# It is also really not recommended to use. But for testing,
# the "__all__" variable is a great feature!
class AllModulesImportTest(unittest.TestCase):
    def testAllModulesCanImport(self):
        # would also work: exec("from PySide6 import *")
        for name in PySide6.__all__:
            exec(f"import PySide6.{name}")

    def testAllReappearsAfterDel(self):
        # This is the only incompatibility that remains:
        # After __all__ is deleted, it will re-appear.
        PySide6.__all__ = 42
        self.assertEqual(PySide6.__dict__["__all__"], 42)
        del PySide6.__all__
        self.assertTrue(PySide6.__dict__["__all__"])
        self.assertNotEqual(PySide6.__dict__["__all__"], 42)


if __name__ == '__main__':
    unittest.main()
