# Copyright (C) 2025 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only
import os

from mainwindow import MainWindow
from PySide6.QtWidgets import QApplication
import sys


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    if os.getenv("PYSIDE_TESTING"):
        return 0
    window.show()
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
