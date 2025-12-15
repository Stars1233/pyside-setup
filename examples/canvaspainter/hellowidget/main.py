# Copyright (C) 2026 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QMdiArea)
from PySide6.QtGui import QKeySequence
from PySide6.QtCore import QCoreApplication, Slot

from canvaswidget import CanvasWidget


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)
        self.createCanvasWidget()

        fileMenu = self.menuBar().addMenu("File")
        fileMenu.addAction("New widget",
                           QKeySequence(QKeySequence.StandardKey.New),
                           self.createCanvasWidget)
        fileMenu.addAction("Exit",
                           QKeySequence(QKeySequence.StandardKey.Quit),
                           qApp.quit)  # noqa: F821

    @Slot()
    def createCanvasWidget(self):
        canvasWidget = CanvasWidget()
        subWin = self.mdi.addSubWindow(canvasWidget)
        subWin.resize(500, 500)
        canvasWidget.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.resize(1280, 720)
    mainWindow.show()
    sys.exit(QCoreApplication.exec())
