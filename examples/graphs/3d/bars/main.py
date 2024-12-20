# Copyright (C) 2024 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

import sys
from pathlib import Path

from PySide6.QtGui import QGuiApplication
from PySide6.QtQuick import QQuickView


if __name__ == '__main__':
    app = QGuiApplication(sys.argv)
    view = QQuickView()

    view.engine().addImportPath(Path(__file__).parent)
    view.loadFromModule("Bars", "Main")
    view.setTitle("Monthly income / expenses")
    view.setResizeMode(QQuickView.ResizeMode.SizeRootObjectToView)
    view.setColor("black")
    view.show()

    ex = app.exec()
    del view
    sys.exit(ex)
