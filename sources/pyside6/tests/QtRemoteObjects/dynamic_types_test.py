#!/usr/bin/python
# Copyright (C) 2025 Ford Motor Company
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only WITH Qt-GPL-exception-1.0
from __future__ import annotations

'''Test cases for dynamic source/replica types'''

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


@wrap_tests_for_cleanup(extra=['rep_file'])
class QDynamicReplicas(unittest.TestCase):
    '''Test case for dynamic Replicas'''

    def setUp(self):
        '''Set up test environment'''
        self.rep_file = RepFile(contents)

    def testDynamicReplica(self):
        '''Verify that a valid Replica is created'''
        Replica = self.rep_file.replica["Simple"]
        self.assertIsNotNone(Replica)
        replica = Replica()
        self.assertIsNotNone(replica)
        self.assertIsNotNone(replica.metaObject())
        meta = replica.metaObject()
        self.assertEqual(meta.className(), "Simple")
        self.assertEqual(meta.superClass().className(), "QRemoteObjectReplica")
        i = meta.indexOfProperty("i")
        self.assertNotEqual(i, -1)
        self.assertEqual(replica.propAsVariant(0), int(2))
        self.assertEqual(replica.propAsVariant(1), float(-1.0))
        self.assertEqual(replica.i, int(2))
        self.assertEqual(replica.f, float(-1.0))


@wrap_tests_for_cleanup(extra=['rep_file'])
class QDynamicSources(unittest.TestCase):
    '''Test case for dynamic Sources'''

    def setUp(self):
        '''Set up test environment'''
        self.rep_file = RepFile(contents)
        self.test_val = 0

    def on_changed(self, val):
        self.test_val = val

    def testDynamicSource(self):
        '''Verify that a valid Source is created'''
        Source = self.rep_file.source["Simple"]
        self.assertIsNotNone(Source)
        source = Source()
        self.assertIsNotNone(source)
        self.assertIsNotNone(source.metaObject())
        meta = source.metaObject()
        self.assertEqual(meta.className(), "SimpleSource")
        self.assertEqual(meta.superClass().className(), "QObject")
        i = meta.indexOfProperty("i")
        self.assertNotEqual(i, -1)
        self.assertIsNotNone(source.__dict__.get('__PROPERTIES__'))
        self.assertEqual(source.i, int(2))
        self.assertEqual(source.f, float(-1.0))
        source.iChanged.connect(self.on_changed)
        source.fChanged.connect(self.on_changed)
        source.i = 7
        self.assertEqual(source.i, int(7))
        self.assertEqual(self.test_val, int(7))
        source.i = 3
        self.assertEqual(self.test_val, int(3))
        source.f = 3.14
        self.assertAlmostEqual(self.test_val, float(3.14), places=5)


if __name__ == '__main__':
    unittest.main()
