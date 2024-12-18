#!/usr/bin/python
# Copyright (C) 2025 Ford Motor Company
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only WITH Qt-GPL-exception-1.0
from __future__ import annotations

'''Test cases for RepFile'''

import os
import sys
import unittest
from pathlib import Path
sys.path.append(os.fspath(Path(__file__).resolve().parents[1]))
from init_paths import init_test_paths
init_test_paths(False)
from PySide6.QtRemoteObjects import RepFile

from test_shared import wrap_tests_for_cleanup

contents = """
class Simple
{
    PROP(int i = 2);
    PROP(float f = -1. READWRITE);
    SIGNAL(random(int i));
    SLOT(void reset());
};
"""


@wrap_tests_for_cleanup()
class QRepFileConstructor(unittest.TestCase):
    '''Test case for RepFile constructors'''
    expected = "RepFile(Classes: [Simple], PODs: [])"

    def setUp(self):
        '''Set up test environment'''
        self.cwd = Path(__file__).parent
        self.path = self.cwd / "simple.rep"

    def testRepFileFromPath(self):
        '''Test constructing RepFile from a path'''
        with open(self.path, 'r') as f:
            rep_file = RepFile(f.read())
        self.assertEqual(str(rep_file), self.expected)

    def testRepFileFromString(self):
        '''Test constructing RepFile from a string'''
        rep_file = RepFile(contents)
        self.assertEqual(str(rep_file), self.expected)

    def testRepFileInvalidString(self):
        '''Test constructing RepFile from a string'''
        with self.assertRaises(RuntimeError) as result:
            RepFile("\n\n}\n\n")
        self.assertEqual(str(result.exception),
                         "Error parsing input, line 3: error: Unknown token encountered")

    def testRepFileNoArguments(self):
        '''Test constructing RepFile with no arguments'''
        with self.assertRaises(TypeError):
            RepFile()


if __name__ == '__main__':
    unittest.main()
