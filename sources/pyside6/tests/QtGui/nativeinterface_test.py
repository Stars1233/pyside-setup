# Copyright (C) 2025 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only WITH Qt-GPL-exception-1.0

import os
import sys
import unittest

from pathlib import Path
sys.path.append(os.fspath(Path(__file__).resolve().parents[1]))
from init_paths import init_test_paths  # noqa: E402
init_test_paths(False)

from PySide6.QtGui import QGuiApplication, QNativeInterface  # noqa
from helper.usesqapplication import UsesQApplication  # noqa: E402


class TestNativeInterface(UsesQApplication):

    @unittest.skipUnless(sys.platform == "linux", "Linux only")
    def testLinuxNativeApplication(self):
        app = qApp  # noqa: F821
        native_app = app.nativeInterface()
        if native_app:
            if issubclass(type(native_app), QNativeInterface.QX11Application):
                self.assertTrue(native_app.display() != 0)


if __name__ == '__main__':
    unittest.main()
