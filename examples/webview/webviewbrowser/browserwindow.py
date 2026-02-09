# Copyright (C) 2026 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

from PySide6.QtCore import QSize, QUrl, Qt, Slot
from PySide6.QtGui import QAction, QIcon, QKeySequence
from PySide6.QtWidgets import (QLineEdit, QMainWindow, QMenu, QProgressBar,
                               QToolButton, QVBoxLayout, QWidget)
from PySide6.QtWebView import QWebView, QWebViewLoadingInfo, QWebViewSettings


URL = "https://qt.io"


PROGRESS_STYLESHEET = "QProgressBar {border: 0px} QProgressBar.chunk {background-color: #da4453}"
SETTINGS_STYLESHEET = "QToolButton::menu-indicator {image: none;}"


SETTINGS = [
    (QWebViewSettings.WebAttribute.LocalStorageEnabled, "Enable Local storage"),
    (QWebViewSettings.WebAttribute.JavaScriptEnabled, "Enable JavaScript"),
    (QWebViewSettings.WebAttribute.AllowFileAccess, "Allow file access"),
    (QWebViewSettings.WebAttribute.LocalContentCanAccessFileUrls,
     "Enable file URLs for local documents")
]


class BrowserWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Set up toolbar
        self._toolBar = self.addToolBar("Navigation")
        self._toolBar.setMovable(False)

        self._backAction = QAction(QIcon(":/images/left-32.png"), "Go back", self)
        self._backAction.setShortcut(QKeySequence.StandardKey.Back)
        self._toolBar.addAction(self._backAction)
        self._forwardAction = QAction(QIcon(":/images/right-32.png"), "Go forward", self)
        self._forwardAction.setShortcut(QKeySequence.StandardKey.Forward)
        self._toolBar.addAction(self._forwardAction)
        self._reloadAction = QAction(QIcon(":/images/refresh-32.png"), "Reload", self)
        self._reloadAction.setShortcut(QKeySequence.StandardKey.Refresh)
        self._toolBar.addAction(self._reloadAction)
        self._stopAction = QAction(QIcon(":/images/stop-32.png"), "Stop", self)
        self._stopAction.setShortcut(QKeySequence.StandardKey.Cancel)
        self._toolBar.addAction(self._stopAction)

        self._toolBar.addSeparator()
        self._lineEdit = QLineEdit(self)
        self._toolBar.addWidget(self._lineEdit)

        centralWidget = QWidget(self)
        layout = QVBoxLayout(centralWidget)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(centralWidget)

        self._progressBar = QProgressBar()
        self._progressBar.setTextVisible(False)
        self._progressBar.setMaximumHeight(2)
        self._progressBar.setStyleSheet(PROGRESS_STYLESHEET)
        layout.addWidget(self._progressBar)

        # Wrap the QWebView in a QWidget
        self._webView = QWebView()
        webViewContainer = QWidget.createWindowContainer(self._webView)
        webViewContainer.setMinimumSize(QSize(1280, 720))
        layout.addWidget(webViewContainer)

        settingsMenuButton = QToolButton()
        settingsMenuButton.setToolTip("Settings")
        settingsMenuButton.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)
        settingsMenuButton.setStyleSheet(SETTINGS_STYLESHEET)
        settingsMenuButton.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        settingsMenuButton.setArrowType(Qt.ArrowType.NoArrow)
        settingsMenuButton.setIcon(QIcon(":/images/settings-32.png"))
        self._toolBar.addSeparator()
        self._toolBar.addWidget(settingsMenuButton)
        settingsMenu = QMenu("Settings", settingsMenuButton)
        settingsMenuButton.setMenu(settingsMenu)
        settings = self._webView.settings()
        for setting in SETTINGS:
            action = settingsMenu.addAction(setting[1])
            attribute = setting[0]
            action.setData(attribute)
            action.setCheckable(True)
            action.setChecked(settings.testAttribute(attribute))
            action.toggled.connect(self.onSettingToggled)

        self._stopAction.setVisible(False)

        # Set up signal/slot connections
        self._backAction.triggered.connect(self._webView.goBack)
        self._forwardAction.triggered.connect(self._webView.goForward)
        self._reloadAction.triggered.connect(self._webView.reload)
        self._stopAction.triggered.connect(self._webView.stop)
        self._webView.loadingChanged.connect(self.onLoadingChanged)
        self._webView.loadProgressChanged.connect(self.onLoadProgressChanged)
        self._webView.titleChanged.connect(self.onTitleChanged)
        self._lineEdit.returnPressed.connect(self.onUrlInput)

        # Load the startup URL
        self._webView.setUrl(QUrl(URL))

    @Slot(QWebViewLoadingInfo)
    def onLoadingChanged(self, loadingInfo):
        match loadingInfo.status():
            case QWebViewLoadingInfo.LoadStatus.Started:
                self._reloadAction.setEnabled(False)
                self._reloadAction.setVisible(False)
                self._stopAction.setEnabled(True)
                self._stopAction.setVisible(True)
            case (QWebViewLoadingInfo.LoadStatus.Stopped | QWebViewLoadingInfo.LoadStatus.Succeeded
                  | QWebViewLoadingInfo.LoadStatus.Failed):
                self._reloadAction.setEnabled(True)
                self._reloadAction.setVisible(True)
                self._stopAction.setEnabled(False)
                self._stopAction.setVisible(False)

        self._backAction.setEnabled(self._webView.canGoBack())
        self._forwardAction.setEnabled(self._webView.canGoForward())
        self._lineEdit.setText(loadingInfo.url().toString())

    @Slot(str)
    def onTitleChanged(self, title):
        self.setWindowTitle(title)

    @Slot(int)
    def onLoadProgressChanged(self, loadProgress):
        value = loadProgress if loadProgress > 0 and loadProgress < 100 else 0
        self._progressBar.setValue(value)

    @Slot()
    def onUrlInput(self):
        self._webView.setUrl(QUrl.fromUserInput(self._lineEdit.text()))

    @Slot(bool)
    def onSettingToggled(self, checked):
        settings = self._webView.settings()
        action = self.sender()
        attribute = action.data()
        settings.setAttribute(attribute, action.isChecked())
        action.setChecked(settings.testAttribute(attribute))
