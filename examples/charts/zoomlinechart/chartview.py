# Copyright (C) 2024 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause
from PySide6.QtCharts import QChart, QChartView
from PySide6.QtGui import QKeyEvent, QMouseEvent
from PySide6.QtCore import QEvent, Qt
from PySide6.QtWidgets import QGraphicsView


class ChartView(QChartView):
    def __init__(self, chart, parent=None):
        super().__init__(chart, parent)

        self.setRubberBand(QChartView.RectangleRubberBand)
        self._isTouching = False

    def viewPortEvent(self, event: QEvent):

        if event.type() == QMouseEvent.TouchBegin:
            self._isTouching = True

            self.chart().setAnimationOptions(QChart.NoAnimation)

        return super().viewPortEvent(event)

    def mousePressEvent(self, event: QMouseEvent):

        if self._isTouching:
            return

        return super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):

        if self._isTouching:
            return

        return super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):

        if self._isTouching:
            self._isTouching = False

        self.chart().setAnimationOptions(QChart.SeriesAnimations)

        return super().mouseReleaseEvent(event)

    def keyPressEvent(self, event: QKeyEvent):

        key = event.key()
        if key == Qt.Key_Plus:
            self.chart().zoomIn()

        elif key == Qt.Key_Minus:
            self.chart().zoomOut()

        elif key == Qt.Key_Left:
            self.chart().scroll(-10, 0)

        elif key == Qt.Key_Right:
            self.chart().scroll(10, 0)

        elif key == Qt.Key_Up:
            self.chart().scroll(0, 10)

        elif key == Qt.Key_Down:
            self.chart().scroll(0, -10)

        else:
            QGraphicsView.keyPressEvent(event)
