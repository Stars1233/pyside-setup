# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only WITH Qt-GPL-exception-1.0
from __future__ import annotations

import os
import sys
import unittest

from pathlib import Path
sys.path.append(os.fspath(Path(__file__).resolve().parents[1]))
from init_paths import init_test_paths
init_test_paths(False)

from PySide6 import *  # noqa: F401,F403
from PySide6.support.signature import get_signature
for modname, mod in sys.modules.items():
    if modname.startswith("PySide6."):
        print("importing", modname)
        exec("import " + modname)

# To help linters
import PySide6.QtCore
import PySide6.QtGui
import PySide6.QtWidgets

# This test tests the existence and callability of the newly existing functions,
# after the inheritance was made complete in the course of PYSIDE-331.

new_functions = """
    PySide6.QtCore.QAbstractItemModel().parent()
    PySide6.QtCore.QAbstractListModel().parent()
    PySide6.QtCore.QAbstractTableModel().parent()
    PySide6.QtCore.QFile().resize(qint64)
    m = PySide6.QtCore.QMutex(); m.tryLock(); m.unlock() # prevent a message "QMutex: destroying locked mutex"
    PySide6.QtCore.QSortFilterProxyModel().parent()
    PySide6.QtCore.QTemporaryFile(tfarg).open(openMode)
"""

new_functions += """
    PySide6.QtGui.QStandardItemModel().insertColumn(_int,qModelIndex)
    PySide6.QtGui.QStandardItemModel().parent()
    # PySide6.QtGui.QTextList(qTextDocument).setFormat(qTextFormat) # Segmentation fault: 11
    # PySide6.QtGui.QTextTable(qTextDocument).setFormat(qTextFormat) # Segmentation fault: 11
""" if "PySide6.QtGui" in sys.modules else ""

new_functions += """
    PySide6.QtWidgets.QAbstractItemView().update()
    PySide6.QtWidgets.QApplication.palette()
    PySide6.QtWidgets.QApplication.setFont(qFont)
    PySide6.QtWidgets.QApplication.setPalette(qPalette)
    PySide6.QtWidgets.QBoxLayout(direction).addWidget(qWidget)
    PySide6.QtWidgets.QColorDialog().open()
    PySide6.QtWidgets.QFileDialog().open()
    PySide6.QtWidgets.QFileSystemModel().index(_int,_int,qModelIndex)
    PySide6.QtWidgets.QFileSystemModel().parent()
    PySide6.QtWidgets.QFontDialog().open()
    PySide6.QtWidgets.QGestureEvent([]).accept()
    PySide6.QtWidgets.QGestureEvent([]).ignore()
    PySide6.QtWidgets.QGestureEvent([]).isAccepted()
    PySide6.QtWidgets.QGestureEvent([]).setAccepted(_bool)
    # PySide6.QtWidgets.QGraphicsView().render(qPaintDevice,qPoint,qRegion,renderFlags) # QPaintDevice: NotImplementedError
    PySide6.QtWidgets.QGridLayout().addWidget(qWidget)
    PySide6.QtWidgets.QInputDialog().open()
    PySide6.QtWidgets.QLineEdit().addAction(qAction)
    PySide6.QtWidgets.QMessageBox().open()
    PySide6.QtWidgets.QPlainTextEdit().find(findStr)
    PySide6.QtWidgets.QProgressDialog().open()
    PySide6.QtWidgets.QStackedLayout().widget()
    # PySide6.QtWidgets.QStylePainter().begin(qPaintDevice) # QPaintDevice: NotImplementedError
    PySide6.QtWidgets.QTextEdit().find(findStr)
    PySide6.QtWidgets.QWidget.find(quintptr)
""" if "PySide6.QtWidgets" in sys.modules else ""

new_functions += """
    # PySide6.QtPrintSupport.QPageSetupDialog().open() # Segmentation fault: 11
    # PySide6.QtPrintSupport.QPrintDialog().open() # opens the dialog, but works
    PySide6.QtPrintSupport.QPrintDialog().printer()
    PySide6.QtPrintSupport.QPrintPreviewDialog().open() # note: this prints something, but really shouldn't ;-)
""" if "PySide6.QtPrintSupport" in sys.modules else ""

new_functions += """
    PySide6.QtHelp.QHelpContentModel().parent()
    # PySide6.QtHelp.QHelpIndexModel().createIndex(_int,_int,quintptr) # returned NULL without setting an error
    # PySide6.QtHelp.QHelpIndexModel().createIndex(_int,_int,object()) # returned NULL without setting an error
""" if "PySide6.QtHelp" in sys.modules else ""

new_functions += """
    PySide6.QtQuick.QQuickPaintedItem().update()
""" if "PySide6.QtQuick" in sys.modules else ""


class MainTest(unittest.TestCase):

    def testNewInheriedFunctionsExist(self):
        """
        Run all new method signarures
        """
        for app in "QtWidgets.QApplication", "QtGui.QGuiApplication", "QtCore.QCoreApplication":
            try:
                exec(f"qApp = PySide6.{app}([]) or PySide6.{app}.instance()")
                break
            except AttributeError:
                continue
        _bool = True  # noqa: F841,F405
        _int = 42  # noqa: F841,F405
        qint64 = 42  # noqa: F841,F405
        tfarg = os.path.join(PySide6.QtCore.QDir.tempPath(), "XXXXXX.tmp")  # noqa: F841,F405
        findStr = 'bla'  # noqa: F841,F405
        orientation = PySide6.QtCore.Qt.Orientations()  # noqa: F841,F405
        openMode = PySide6.QtCore.QIODevice.OpenMode(PySide6.QtCore.QIODevice.ReadOnly)  # noqa: F841,F405
        qModelIndex = PySide6.QtCore.QModelIndex()  # noqa: F841,F405
        transformationMode = PySide6.QtCore.Qt.TransformationMode()  # noqa: F841,F405
        qObject = PySide6.QtCore.QObject()  # noqa: F841,F405
        qPoint = PySide6.QtCore.QPoint()  # noqa: F841,F405
        try:
            PySide6.QtGui  # noqa: F405
            #qPaintDevice = PySide6.QtGui.QPaintDevice()  # NotImplementedError
            qTextDocument = PySide6.QtGui.QTextDocument()  # noqa: F841,F405
            qTextFormat = PySide6.QtGui.QTextFormat()  # noqa: F841,F405
            quintptr = 42  # noqa: F841,F405
            qFont = PySide6.QtGui.QFont()  # noqa: F841,F405
            qPalette = PySide6.QtGui.QPalette()  # noqa: F841,F405
        except AttributeError:
            pass
        try:
            PySide6.QtWidgets  # noqa: F405
            direction = PySide6.QtWidgets.QBoxLayout.Direction()  # noqa: F841,F405
            qWidget = PySide6.QtWidgets.QWidget()  # noqa: F841,F405
            qStyleOptionFrame = PySide6.QtWidgets.QStyleOptionFrame()  # noqa: F841,F405
            qAction = PySide6.QtGui.QAction(qObject)  # noqa: F841,F405
            renderFlags = PySide6.QtWidgets.QWidget.RenderFlags  # noqa: F841,F405
        except AttributeError:
            pass

        for func in new_functions.splitlines():
            func = func.strip()
            if func.startswith("#"):
                # this is a crashing or otherwise untestable function
                print(func)
                continue
            try:
                exec(func)
            except NotImplementedError:
                print(func, "# raises NotImplementedError")
            else:
                print(func)

    def testQAppSignatures(self):
        """
        Verify that qApp.palette owns three signatures, especially
        palette() without argument.
        """
        try:
            qApp = (  # noqa: F841
                PySide6.QtWidgets.QApplication.instance() or PySide6.QtWidgets.QApplication([])  # noqa: F405
            )
        except AttributeError:
            unittest.TestCase().skipTest("this test makes only sense if QtWidgets is available.")

        sigs = get_signature(PySide6.QtWidgets.QApplication.palette)  # noqa: F405
        self.assertEqual(len(sigs), 3)


if __name__ == '__main__':
    unittest.main()
