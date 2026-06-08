# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only WITH Qt-GPL-exception-1.0
from __future__ import annotations

import gc
import os
import sys
import unittest

from collections import Counter
from pathlib import Path
from typing import Union
sys.path.append(os.fspath(Path(__file__).resolve().parents[1]))
from init_paths import init_test_paths
init_test_paths(False)

from PySide6.QtCore import QObject
from PySide6.QtGui import QStandardItemModel, QStandardItem
from shiboken6 import Shiboken
from helper.usesqapplication import UsesQApplication


def get_standarditem_count() -> int:
    return Counter([obj.__class__ for obj in gc.get_objects()])[QStandardItem]


def create_row(prefix: str) -> list:
    return [QStandardItem(prefix + "_1"), QStandardItem(prefix + "_2")]


# Helper functions for QStandardItemModelRef.testRemoval().
def populate_tree_model(root: Union[QStandardItem, QStandardItemModel]) -> None:
    for t in range(5):
        row = create_row(f"top{t}")
        root.appendRow(row)
        for c in range(10):
            row[0].appendRow(create_row(f"child{c}"))


def create_tree_model() -> QStandardItemModel:
    result = QStandardItemModel(0, 2)
    populate_tree_model(result)
    return result


def create_tree_model_root_item() -> QStandardItemModel:
    result = QStandardItemModel(0, 2)
    populate_tree_model(result.invisibleRootItem())
    return result


def clear_model_clear(model: QStandardItemModel):
    model.clear()


def clear_model_setRowCount(model: QStandardItemModel):
    model.setRowCount(0)


def clear_model_removeRows(model: QStandardItemModel):
    model.removeRows(0, model.rowCount())


class QStandardItemModelTest(UsesQApplication):

    def setUp(self):
        super(QStandardItemModelTest, self).setUp()
        self.parent = QObject()
        self.model = QStandardItemModel(0, 3, self.parent)

    def tearDown(self):
        del self.parent
        del self.model
        # PYSIDE-535: Need to collect garbage in PyPy to trigger deletion
        gc.collect()
        super(QStandardItemModelTest, self).tearDown()

    def testInsertRow(self):
        # bug #227
        self.model.insertRow(0)

    def testClear(self):

        model = QStandardItemModel()
        root = model.invisibleRootItem()
        model.clear()
        self.assertFalse(Shiboken.isValid(root))


class QStandardItemModelRef(UsesQApplication):
    @unittest.skipUnless(hasattr(sys, "getrefcount"), f"{sys.implementation.name} has no refcount")
    def testRefCount(self):
        model = QStandardItemModel(5, 5)
        items = []
        for r in range(5):
            row = []
            for c in range(5):
                row.append(QStandardItem(f"{r},{c}"))
                self.assertEqual(sys.getrefcount(row[c]), 2)

            model.insertRow(r, row)

            for c in range(5):
                ref_after = sys.getrefcount(row[c])
                # check if the ref count was incremented after insertRow
                self.assertEqual(ref_after, 3)

            items.append(row)
            row = None

        for r in range(3):
            my_row = model.takeRow(0)
            my_row = None  # noqa: F841
            for c in range(5):
                # only rest 1 reference
                self.assertEqual(sys.getrefcount(items[r][c]), 2)

        my_i = model.item(0, 0)
        # ref(my_i) + parent_ref + items list ref
        base_ref_count = 2 if sys.version_info >= (3, 14) else 3
        self.assertEqual(sys.getrefcount(my_i), base_ref_count + 1)

        model.clear()
        # ref(my_i)
        self.assertEqual(sys.getrefcount(my_i), base_ref_count)

    def testRemoval(self):
        """PYSIDE-3365: Test that no items are leaked when creating them
           either by appending to the model or its invisible root item."""
        creation_funcs = [create_tree_model, create_tree_model_root_item]
        clear_funcs = [clear_model_clear, clear_model_setRowCount, clear_model_removeRows]

        for creation_func in creation_funcs:
            for clear_func in clear_funcs:
                old_count = get_standarditem_count()
                model = creation_func()
                clear_func(model)
                cleared_count = get_standarditem_count()
                self.assertEqual(old_count, cleared_count,
                                 creation_func.__name__ + '/' + clear_func.__name__)


if __name__ == '__main__':
    unittest.main()
