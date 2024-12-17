# Copyright (C) 2024 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only WITH Qt-GPL-exception-1.0
from __future__ import annotations

'''Unit test for WebView'''

import os
import sys
import unittest
from pathlib import Path

# Append the necessary paths to sys.path
sys.path.append(os.fspath(Path(__file__).resolve().parents[1]))
from init_paths import init_test_paths
init_test_paths(False)

from PySide6.QtWebView import QtWebView

from helper.usesqapplication import UsesQApplication


class QWebViewTestCase(UsesQApplication):
    def test_webview_exists(self):
        # Initialize QtWebView
        QtWebView.initialize()

        # Check if QtWebView can be initialized
        self.assertTrue(QtWebView is not None)
        print("QtWebView is available in PySide6.")


if __name__ == "__main__":
    unittest.main()
