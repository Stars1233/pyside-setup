# Copyright (C) 2026 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

import sys
from PySide6.QtWidgets import QApplication

import rc_webviewbrowser  # noqa: F401
from browserwindow import BrowserWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browserWindow = BrowserWindow()
    browserWindow.show()
    sys.exit(app.exec())
