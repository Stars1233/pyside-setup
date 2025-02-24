# Copyright (C) 2025 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only
from PySide6.QtWidgets import QPushButton, QApplication
import sys


class SubprojectButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.setText("Subproject button")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    button = SubprojectButton()
    button.show()
    sys.exit(app.exec())
