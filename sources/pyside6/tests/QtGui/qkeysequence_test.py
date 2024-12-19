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

from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, qt_set_sequence_auto_mnemonic

from helper.usesqapplication import UsesQApplication


class QKeySequenceTest(UsesQApplication):

    def testGetItemOperator(self):
        # bug #774
        # PYSIDE-1735: Remapped from Qt.Modifier to Qt.KeyboardModifier
        #              Note that Qt.(Keyboard)?Modifier will be no longer IntFlag.
        ks = QKeySequence(Qt.KeyboardModifier.ShiftModifier, Qt.KeyboardModifier.ControlModifier,
                          Qt.Key.Key_P, Qt.Key.Key_R)
        self.assertEqual(ks[0].keyboardModifiers(), Qt.KeyboardModifier.ShiftModifier)
        self.assertEqual(ks[1].keyboardModifiers(), Qt.KeyboardModifier.ControlModifier)
        self.assertEqual(ks[2].key(), Qt.Key.Key_P)
        self.assertEqual(ks[3].key(), Qt.Key.Key_R)

        def testAutoMnemonic(self):
            qt_set_sequence_auto_mnemonic(True)


if __name__ == '__main__':
    unittest.main()
