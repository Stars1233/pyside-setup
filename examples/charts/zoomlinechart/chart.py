# Copyright (C) 2024 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause
from PySide6.QtWidgets import QGesture, QGestureEvent
from PySide6.QtCore import Qt, QEvent
from PySide6.QtCharts import QChart


class Chart(QChart):
    def __init__(self,
                 ChartType=QChart.ChartType.ChartTypeCartesian,
                 QGraphicsItem=None,
                 WindowType=Qt.WindowFlags):
        super().__init__()

        self.grabGesture(Qt.PanGesture)
        self.grabGesture(Qt.PinchGesture)

    def sceneEvent(self, event: QEvent):

        if event.type() == QEvent.Gesture:
            return self.gestureEvent(event)

        return super().sceneEvent(event)

    def gestureEvent(self, event: QGestureEvent):

        if gesture := event.gesture(Qt.PanGesture):
            pan = gesture
            self.scroll(-pan.delta().x(), pan.delta().y())

        if gesture := event.gesture(Qt.PinchGesture):
            pinch = gesture

            if pinch.changeFlags() & QGesture.QPinchGesture.ScaleFactorChanged:
                self.zoom(pinch.scaleFactor())

        return True
