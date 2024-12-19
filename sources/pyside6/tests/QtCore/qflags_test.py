#!/usr/bin/python
# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only WITH Qt-GPL-exception-1.0
from __future__ import annotations

'''Test cases for QFlags'''

import os
import sys
import unittest

from pathlib import Path
sys.path.append(os.fspath(Path(__file__).resolve().parents[1]))
from init_paths import init_test_paths
init_test_paths(False)

from PySide6.QtCore import Qt, QTemporaryFile, QFile, QIODevice, QObject


class QFlagTest(unittest.TestCase):
    '''Test case for usage of flags'''

    def testCallFunction(self):
        f = QTemporaryFile()
        self.assertTrue(f.open())
        fileName = f.fileName()
        f.close()

        f = QFile(fileName)
        of = (QIODevice.OpenModeFlag.Truncate | QIODevice.OpenModeFlag.Text
              | QIODevice.OpenModeFlag.ReadWrite)
        self.assertEqual(f.open(of), True)
        om = f.openMode()
        self.assertEqual(om & QIODevice.OpenModeFlag.Truncate, QIODevice.OpenModeFlag.Truncate)
        self.assertEqual(om & QIODevice.OpenModeFlag.Text, QIODevice.OpenModeFlag.Text)
        self.assertEqual(om & QIODevice.OpenModeFlag.ReadWrite, QIODevice.OpenModeFlag.ReadWrite)
        expected = (QIODevice.OpenModeFlag.Truncate | QIODevice.OpenModeFlag.Text
                    | QIODevice.OpenModeFlag.ReadWrite)
        self.assertTrue(om == expected)
        f.close()


class QFlagOperatorTest(unittest.TestCase):
    '''Test case for operators in QFlags'''

    def testInvert(self):
        '''QFlags ~ (invert) operator'''
        self.assertEqual(type(~QIODevice.OpenModeFlag.ReadOnly), QIODevice.OpenMode)

    def testOr(self):
        '''QFlags | (or) operator'''
        self.assertEqual(type(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.WriteOnly),
                         QIODevice.OpenMode)

    def testAnd(self):
        '''QFlags & (and) operator'''
        self.assertEqual(type(QIODevice.OpenModeFlag.ReadOnly & QIODevice.OpenModeFlag.WriteOnly),
                         QIODevice.OpenMode)

    def testIOr(self):
        '''QFlags |= (ior) operator'''
        flag = Qt.WindowFlags()
        self.assertTrue(Qt.WindowType.Widget == 0)
        self.assertFalse(flag & Qt.WindowType.Widget)
        result = flag & Qt.WindowType.Widget
        self.assertTrue(result == 0)
        flag |= Qt.WindowType.WindowMinimizeButtonHint
        self.assertTrue(flag & Qt.WindowType.WindowMinimizeButtonHint)

    def testInvertOr(self):
        '''QFlags ~ (invert) operator over the result of an | (or) operator'''
        self.assertEqual(type(~(Qt.ItemFlag.ItemIsSelectable | Qt.ItemFlag.ItemIsEditable)),
                         Qt.ItemFlags)

    def testEqual(self):
        '''QFlags == operator'''
        flags = Qt.WindowType.Window
        flags |= Qt.WindowType.WindowMinimizeButtonHint
        flag_type = (flags & Qt.WindowType.WindowType_Mask)
        self.assertEqual(flag_type, Qt.WindowType.Window)

        self.assertEqual(Qt.KeyboardModifiers(Qt.KeyboardModifier.ControlModifier),
                         Qt.KeyboardModifier.ControlModifier)

    def testOperatorBetweenFlags(self):
        '''QFlags & QFlags'''
        flags = Qt.ItemFlag.NoItemFlags | Qt.ItemFlag.ItemIsUserCheckable
        newflags = Qt.ItemFlag.NoItemFlags | Qt.ItemFlag.ItemIsUserCheckable
        self.assertTrue(flags & newflags)

    def testOperatorDifferentOrder(self):
        '''Different ordering of arguments'''
        flags = Qt.ItemFlag.NoItemFlags | Qt.ItemFlag.ItemIsUserCheckable
        self.assertEqual(flags | Qt.ItemFlag.ItemIsEnabled, Qt.ItemFlag.ItemIsEnabled | flags)

    def testEqualNonNumericalObject(self):
        '''QFlags ==,!= non-numerical object '''
        flags = Qt.ItemFlag.NoItemFlags | Qt.ItemFlag.ItemIsUserCheckable

        self.assertTrue(flags != None)  # noqa: E711
        self.assertFalse(flags == None)  # noqa: E711

        self.assertTrue(flags != "tomato")
        self.assertFalse(flags == "tomato")

        with self.assertRaises(TypeError):
            flags > None
        with self.assertRaises(TypeError):
            flags >= None
        with self.assertRaises(TypeError):
            flags < None
        with self.assertRaises(TypeError):
            flags <= None


class QFlagsOnQVariant(unittest.TestCase):
    def testQFlagsOnQVariant(self):
        o = QObject()
        o.setProperty("foo", QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.WriteOnly)
        self.assertEqual(type(o.property("foo")), QIODevice.OpenMode)


class QEnumFlagDefault(unittest.TestCase):
    """
        Check that old flag and enum syntax can be used.
        The signatures of these surrogate functions intentionally do not exist
        because people should learn to use the new Enums correctly.
    """
    def testOldQFlag(self):
        self.assertEqual(Qt.AlignmentFlag(), Qt.AlignmentFlag(0))
        oldFlag = Qt.Alignment()
        oldEnum = Qt.AlignmentFlag()
        self.assertEqual(type(oldFlag), Qt.Alignment)
        self.assertEqual(type(oldEnum), Qt.AlignmentFlag)
        self.assertEqual(type(oldFlag), type(oldEnum))


if __name__ == '__main__':
    unittest.main()
