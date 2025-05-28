# Copyright (C) 2023 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause
from __future__ import annotations

import sys

from pathlib import Path

from PySide6.QtCore import QFile, QIODevice, QObject, QRangeModel
from PySide6.QtGraphs import (QBar3DSeries, QCategory3DAxis, QValue3DAxis, QItemModelBarDataProxy)


MONTHS = ["January", "February", "March", "April",
          "May", "June", "July", "August", "September", "October",
          "November", "December"]


def read_data(file_path):
    """Return a tuple of data matrix/first year."""
    dataFile = QFile(file_path)
    if not dataFile.open(QIODevice.OpenModeFlag.ReadOnly | QIODevice.OpenModeFlag.Text):
        print("Unable to open data file:", dataFile.fileName(), file=sys.stderr)
        return None, None

    last_year = -1
    first_year = -1
    result = []
    data = dataFile.readAll().data().decode("utf8")
    for line in data.split("\n"):
        if line and not line.startswith("#"):  # Ignore comments
            tokens = line.split(",")
            # Each line has three data items: Year, month, and
            # rainfall value
            if len(tokens) >= 3:
                # Store year and month as strings, and rainfall value
                # as double into a variant data item and add the item to
                # the item list.
                year = int(tokens[0].strip())
                month = int(tokens[1].strip())
                value = float(tokens[2].strip())
                if year != last_year:
                    if first_year == -1:
                        first_year = last_year
                    result.append([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
                    last_year = year
                yearly_values = result[len(result) - 1]
                yearly_values[month - 1] = value

    return result, first_year


class RainfallData(QObject):

    def __init__(self):
        super().__init__()
        self._columnCount = 0
        self._rowCount = 0
        self._years = []
        self._numericMonths = []
        self._mapping = None
        self._series = QBar3DSeries()
        self._valueAxis = QValue3DAxis()
        self._rowAxis = QCategory3DAxis()
        self._colAxis = QCategory3DAxis()

        # In data file the months are in numeric format, so create custom list
        for i in range(1, 13):
            self._numericMonths.append(str(i))

        self._columnCount = len(self._numericMonths)

        file_path = Path(__file__).resolve().parent / "data" / "raindata.txt"
        values, first_year = read_data(file_path)
        assert (values)
        self.updateYearsList(first_year, first_year + len(values))
        self._model = QRangeModel(values, self)
        self._proxy = QItemModelBarDataProxy(self._model)
        self._proxy.setUseModelCategories(True)
        self._series = QBar3DSeries(self._proxy)

        self._series.setItemLabelFormat("%.1f mm")

        # Create the axes
        self._rowAxis = QCategory3DAxis(self)
        self._colAxis = QCategory3DAxis(self)
        self._valueAxis = QValue3DAxis(self)
        self._rowAxis.setAutoAdjustRange(True)
        self._colAxis.setAutoAdjustRange(True)
        self._valueAxis.setAutoAdjustRange(True)

        # Set axis labels and titles
        self._rowAxis.setTitle("Year")
        self._colAxis.setTitle("Month")
        self._valueAxis.setTitle("rainfall (mm)")
        self._valueAxis.setSegmentCount(5)
        self._rowAxis.setLabels(self._years)
        self._colAxis.setLabels(MONTHS)
        self._rowAxis.setTitleVisible(True)
        self._colAxis.setTitleVisible(True)
        self._valueAxis.setTitleVisible(True)

    def customSeries(self):
        return self._series

    def valueAxis(self):
        return self._valueAxis

    def rowAxis(self):
        return self._rowAxis

    def colAxis(self):
        return self._colAxis

    def updateYearsList(self, start, end):
        self._years.clear()
        for i in range(start, end + 1):
            self._years.append(str(i))
        self._rowCount = len(self._years)
