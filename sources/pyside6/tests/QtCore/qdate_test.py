#!/usr/bin/python
# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only WITH Qt-GPL-exception-1.0
from __future__ import annotations

'''Test cases for QDate'''

import datetime
import os
import sys
import unittest

from pathlib import Path
sys.path.append(os.fspath(Path(__file__).resolve().parents[1]))
from init_paths import init_test_paths
init_test_paths(False)

from PySide6.QtCore import QDate


class TestQDate (unittest.TestCase):
    def testGetDate(self):
        date = QDate(2009, 22, 9)
        tuple_ = date.getDate()
        self.assertEqual(tuple, tuple_.__class__)
        (y, m, d) = tuple_
        self.assertEqual(date.year(), y)
        self.assertEqual(date.month(), m)
        self.assertEqual(date.day(), d)

    def testGetWeekNumber(self):
        date = QDate(2000, 1, 1)
        tuple_ = date.weekNumber()
        self.assertEqual(tuple, tuple_.__class__)
        (week, yearNumber) = tuple_
        self.assertEqual(week, 52)
        self.assertEqual(yearNumber, 1999)

    def testBooleanCast(self):
        today = QDate.currentDate()
        self.assertTrue(today)
        nodate = QDate()
        self.assertFalse(nodate)


class TestQDateConversion(unittest.TestCase):
    def testDateConversion(self):
        qdate = QDate(1993, 5, 1)
        qdatePy = QDate(datetime.date(1993, 5, 1))
        self.assertEqual(qdate, qdatePy)

    def testDateTimeConversion(self):
        qdate = QDate(2003, 5, 1)
        qdatePy = QDate(datetime.datetime(2003, 5, 1, 11, 1, 14))
        self.assertEqual(qdate, qdatePy)


if __name__ == '__main__':
    unittest.main()
