# Copyright (C) 2024 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause
import sys
import math
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt, QPointF, QRandomGenerator
from PySide6.QtCharts import QChart, QLineSeries
from PySide6.QtGui import QPainter

import chartview
import chart

if __name__ == "__main__":

    app = QApplication(sys.argv)

    series = QLineSeries()

    points = [
        QPointF(float(i), math.sin(math.pi / 50 * i) * 100 + QRandomGenerator.global_().bounded(20))
        for i in range(500)]

    series.append(points)

    line_chart = chart.Chart()
    line_chart.addSeries(series)
    line_chart.setTitle("Zoom in/out example")
    line_chart.setAnimationOptions(QChart.SeriesAnimations)
    line_chart.legend().hide()
    line_chart.createDefaultAxes()

    chart_view = chartview.ChartView(line_chart)
    chart_view.setRenderHint(QPainter.Antialiasing, True)

    window = QMainWindow()
    window.setCentralWidget(chart_view)
    window.resize(400, 300)
    window.grabGesture(Qt.PanGesture)
    window.grabGesture(Qt.PinchGesture)
    window.show()

    sys.exit(app.exec())
