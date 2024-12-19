#!/usr/bin/python
# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only WITH Qt-GPL-exception-1.0
from __future__ import annotations

'''Test cases for QtCore.QEvent'''

import os
import sys
import unittest

from pathlib import Path
sys.path.append(os.fspath(Path(__file__).resolve().parents[1]))
from init_paths import init_test_paths
init_test_paths(False)

from PySide6.QtCore import QEvent


class QEventTypeFlag(unittest.TestCase):
    '''Test case for usage of QEvent.Type flags'''

    def testFlagAccess(self):
        # QEvent.Type flags usage

        event = QEvent(QEvent.Type.Timer)
        self.assertEqual(event.type(), QEvent.Type.Timer)

        event = QEvent(QEvent.Type.Close)
        self.assertEqual(event.type(), QEvent.Type.Close)

        event = QEvent(QEvent.Type.IconTextChange)
        self.assertEqual(event.type(), QEvent.Type.IconTextChange)


if __name__ == '__main__':
    unittest.main()
