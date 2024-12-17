# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause
from __future__ import annotations

import sys

from PySide6.QtCore import QPoint, QTimer, QTime, Qt
from PySide6.QtGui import (QGuiApplication, QPainter, QPainterStateGuard,
                           QPalette, QPolygon, QRasterWindow)

"""Simplified PySide6 port of the gui/analogclock example from Qt v6.x"""


class AnalogClockWindow(QRasterWindow):

    def __init__(self):
        super().__init__()
        self.setTitle("Analog Clock")
        self.resize(200, 200)

        self._timer = QTimer(self)
        self._timer.timeout.connect(self.update)
        self._timer.start(1000)

        self._hour_hand = QPolygon([QPoint(5, 14), QPoint(-5, 14),
                                    QPoint(-4, -71), QPoint(4, -71)])
        self._minute_hand = QPolygon([QPoint(4, 14), QPoint(-4, 14),
                                      QPoint(-3, -89), QPoint(3, -89)])
        self._seconds_hand = QPolygon([QPoint(1, 14), QPoint(-1, 14),
                                       QPoint(-1, -89), QPoint(1, -89)])

        palette = qApp.palette()  # noqa: F821
        self._background_color = palette.color(QPalette.ColorRole.Window)
        self._hour_color = palette.color(QPalette.ColorRole.Text)
        self._minute_color = palette.color(QPalette.ColorRole.Text)
        self._seconds_color = palette.color(QPalette.ColorRole.Accent)

    def paintEvent(self, e):
        with QPainter(self) as painter:
            self.render(painter)

    def render(self, painter):
        width = self.width()
        height = self.height()

        side = min(width, height)

        painter.fillRect(0, 0, width, height, self._background_color)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.translate(width / 2, height / 2)
        painter.scale(side / 200.0, side / 200.0)

        time = QTime.currentTime()

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self._hour_color)

        with QPainterStateGuard(painter):
            painter.rotate(30.0 * ((time.hour() + time.minute() / 60.0)))
            painter.drawConvexPolygon(self._hour_hand)

        for _ in range(0, 12):
            painter.drawRect(73, -3, 16, 6)
            painter.rotate(30.0)

        painter.setBrush(self._minute_color)

        with QPainterStateGuard(painter):
            painter.rotate(6.0 * time.minute())
            painter.drawConvexPolygon(self._minute_hand)

        painter.setBrush(self._seconds_color)

        with QPainterStateGuard(painter):
            painter.rotate(6.0 * time.second())
            painter.drawConvexPolygon(self._seconds_hand)
            painter.drawEllipse(-3, -3, 6, 6)
            painter.drawEllipse(-5, -68, 10, 10)

        painter.setPen(self._minute_color)

        for _ in range(0, 60):
            painter.drawLine(92, 0, 96, 0)
            painter.rotate(6.0)


if __name__ == "__main__":
    app = QGuiApplication(sys.argv)
    clock = AnalogClockWindow()
    clock.show()
    sys.exit(app.exec())
