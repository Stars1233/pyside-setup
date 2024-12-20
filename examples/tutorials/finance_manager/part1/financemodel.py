# Copyright (C) 2024 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

from datetime import datetime
from dataclasses import dataclass
from enum import IntEnum
from collections import defaultdict

from PySide6.QtCore import (QAbstractListModel, QEnum, Qt, QModelIndex, Slot,
                            QByteArray)
from PySide6.QtQml import QmlElement

QML_IMPORT_NAME = "Finance"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class FinanceModel(QAbstractListModel):

    @QEnum
    class FinanceRole(IntEnum):
        ItemNameRole = Qt.ItemDataRole.DisplayRole
        CategoryRole = Qt.ItemDataRole.UserRole
        CostRole = Qt.ItemDataRole.UserRole + 1
        DateRole = Qt.ItemDataRole.UserRole + 2
        MonthRole = Qt.ItemDataRole.UserRole + 3

    @dataclass
    class Finance:
        item_name: str
        category: str
        cost: float
        date: str

        @property
        def month(self):
            return datetime.strptime(self.date, "%d-%m-%Y").strftime("%B %Y")

    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.m_finances = []
        self.m_finances.append(self.Finance("Mobile Prepaid", "Electronics", 20.00, "15-02-2024"))
        self.m_finances.append(self.Finance("Groceries-Feb-Week1", "Groceries", 60.75,
                                            "16-01-2024"))
        self.m_finances.append(self.Finance("Bus Ticket", "Transport", 5.50, "17-01-2024"))
        self.m_finances.append(self.Finance("Book", "Education", 25.00, "18-01-2024"))

    def rowCount(self, parent=QModelIndex()):
        return len(self.m_finances)

    def data(self, index: QModelIndex, role: int):
        row = index.row()
        if row < self.rowCount():
            finance = self.m_finances[row]
            if role == FinanceModel.FinanceRole.ItemNameRole:
                return finance.item_name
            if role == FinanceModel.FinanceRole.CategoryRole:
                return finance.category
            if role == FinanceModel.FinanceRole.CostRole:
                return finance.cost
            if role == FinanceModel.FinanceRole.DateRole:
                return finance.date
            if role == FinanceModel.FinanceRole.MonthRole:
                return finance.month
        return None

    @Slot(result=dict)
    def getCategoryData(self):
        category_data = defaultdict(float)
        for finance in self.m_finances:
            category_data[finance.category] += finance.cost
        return dict(category_data)

    def roleNames(self):
        roles = super().roleNames()
        roles[FinanceModel.FinanceRole.ItemNameRole] = QByteArray(b"item_name")
        roles[FinanceModel.FinanceRole.CategoryRole] = QByteArray(b"category")
        roles[FinanceModel.FinanceRole.CostRole] = QByteArray(b"cost")
        roles[FinanceModel.FinanceRole.DateRole] = QByteArray(b"date")
        roles[FinanceModel.FinanceRole.MonthRole] = QByteArray(b"month")
        return roles

    @Slot(int, result='QVariantMap')
    def get(self, row: int):
        finance = self.m_finances[row]
        return {"item_name": finance.item_name, "category": finance.category,
                "cost": finance.cost, "date": finance.date}

    @Slot(str, str, float, str)
    def append(self, item_name: str, category: str, cost: float, date: str):
        finance = self.Finance(item_name, category, cost, date)
        self.beginInsertRows(QModelIndex(), 0, 0)  # Insert at the front
        self.m_finances.insert(0, finance)  # Insert at the front of the list
        self.endInsertRows()
