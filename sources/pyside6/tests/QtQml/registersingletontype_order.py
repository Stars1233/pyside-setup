# Copyright (C) 2026 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only WITH Qt-GPL-exception-1.0

import os
import sys
import unittest

from pathlib import Path
sys.path.append(os.fspath(Path(__file__).resolve().parents[1]))
from init_paths import init_test_paths  # noqa: E402
init_test_paths(False)

from PySide6.QtCore import QCoreApplication, QObject  # noqa: E402
from PySide6.QtQml import qmlRegisterSingletonType, QQmlComponent, QQmlEngine  # noqa: E402


class MySingleton(QObject):
    def __init__(self, p=None):
        super().__init__(p)


TEST_CODE = """
import QtQuick

Item {
   Rectangle {
   }
}
"""


class Test(unittest.TestCase):
    """PYSIDE-3374: Registering singletons after QQmlEngine instantiation
       used to cause errors while component loading, for example:
       'Cannot assign object of type "QQuickRectangle" to list property "data";
        expected "QObject".' """
    def test(self):
        app = QCoreApplication([])  # noqa: F841

        engine = QQmlEngine()
        qmlRegisterSingletonType(MySingleton, "MyModule", 1, 0, "MySingleton")

        component = QQmlComponent(engine)
        component.setData(TEST_CODE.encode(), ".")

        self.assertFalse(component.isError(), component.errorString())


if __name__ == '__main__':
    unittest.main()
