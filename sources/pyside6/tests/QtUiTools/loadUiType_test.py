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

from helper.usesqapplication import UsesQApplication

from PySide6.QtCore import QStandardPaths
from PySide6.QtWidgets import QWidget, QFrame, QPushButton
from PySide6.QtUiTools import loadUiType


class loadUiTypeTester(UsesQApplication):

    @unittest.skipUnless(bool(QStandardPaths.findExecutable("pyside6-uic")), "pyside6-uic missing")
    def testFunction(self):
        test_dir = Path(__file__).parent.resolve()
        filePath = test_dir / "minimal.ui"
        loaded = loadUiType(os.fspath(filePath))
        self.assertNotEqual(loaded, None)

        # (<class '__main__.Ui_Form'>, <class 'PySide6.QtWidgets.QFrame'>)
        generated, base = loaded

        # Generated class contains retranslateUi method
        self.assertTrue("retranslateUi" in dir(generated))

        # Base class instance will be QFrame for this example
        self.assertTrue(isinstance(base(), QFrame))

        anotherFileName = test_dir / "test.ui"
        another = loadUiType(os.fspath(anotherFileName))
        self.assertNotEqual(another, None)

        generated, base = another
        # Base class instance will be QWidget for this example
        self.assertTrue(isinstance(base(), QWidget))

        w = base()
        ui = generated()
        ui.setupUi(w)

        self.assertTrue(isinstance(ui.child_object, QFrame))
        self.assertTrue(isinstance(ui.grandson_object, QPushButton))

        invalidFileName = test_dir / "invalid.ui"
        loaded = loadUiType(os.fspath(invalidFileName))
        self.assertEqual(loaded, None)


if __name__ == '__main__':
    unittest.main()
