# Copyright (C) 2025 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from folder.label_in_folder import LabelInFolder
from subproject.subproject_button import SubprojectButton


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Main Window")

        self.central_layout = QVBoxLayout()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.central_layout)

        self.label_in_folder = LabelInFolder()
        self.central_layout.addWidget(self.label_in_folder)

        self.subproject_button = SubprojectButton()
        self.central_layout.addWidget(self.subproject_button)
