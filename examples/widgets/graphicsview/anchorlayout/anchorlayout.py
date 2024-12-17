# Copyright (C) 2013 Riverbank Computing Limited.
# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause
from __future__ import annotations

import sys

from PySide6.QtCore import QSizeF, Qt
from PySide6.QtWidgets import (QApplication, QGraphicsAnchorLayout,
                               QGraphicsProxyWidget, QGraphicsScene,
                               QGraphicsView, QGraphicsWidget,
                               QPushButton, QSizePolicy)


def create_item(minimum, preferred, maximum, name):
    w = QGraphicsProxyWidget()

    w.setWidget(QPushButton(name))
    w.setMinimumSize(minimum)
    w.setPreferredSize(preferred)
    w.setMaximumSize(maximum)
    w.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)

    return w


if __name__ == '__main__':
    app = QApplication(sys.argv)

    scene = QGraphicsScene()
    scene.setSceneRect(0, 0, 800, 480)

    min_size = QSizeF(30, 100)
    pref_size = QSizeF(210, 100)
    max_size = QSizeF(300, 100)

    a = create_item(min_size, pref_size, max_size, "A")
    b = create_item(min_size, pref_size, max_size, "B")
    c = create_item(min_size, pref_size, max_size, "C")
    d = create_item(min_size, pref_size, max_size, "D")
    e = create_item(min_size, pref_size, max_size, "E")
    f = create_item(QSizeF(30, 50), QSizeF(150, 50), max_size, "F")
    g = create_item(QSizeF(30, 50), QSizeF(30, 100), max_size, "G")

    l = QGraphicsAnchorLayout()  # noqa: E741
    l.setSpacing(0)

    w = QGraphicsWidget(None, Qt.WindowType.Window)
    w.setPos(20, 20)
    w.setLayout(l)

    # Vertical
    l.addAnchor(a, Qt.AnchorPoint.AnchorTop, l, Qt.AnchorPoint.AnchorTop)
    l.addAnchor(b, Qt.AnchorPoint.AnchorTop, l, Qt.AnchorPoint.AnchorTop)

    l.addAnchor(c, Qt.AnchorPoint.AnchorTop, a, Qt.AnchorPoint.AnchorBottom)
    l.addAnchor(c, Qt.AnchorPoint.AnchorTop, b, Qt.AnchorPoint.AnchorBottom)
    l.addAnchor(c, Qt.AnchorPoint.AnchorBottom, d, Qt.AnchorPoint.AnchorTop)
    l.addAnchor(c, Qt.AnchorPoint.AnchorBottom, e, Qt.AnchorPoint.AnchorTop)

    l.addAnchor(d, Qt.AnchorPoint.AnchorBottom, l, Qt.AnchorPoint.AnchorBottom)
    l.addAnchor(e, Qt.AnchorPoint.AnchorBottom, l, Qt.AnchorPoint.AnchorBottom)

    l.addAnchor(c, Qt.AnchorPoint.AnchorTop, f, Qt.AnchorPoint.AnchorTop)
    l.addAnchor(c, Qt.AnchorPoint.AnchorVerticalCenter, f, Qt.AnchorPoint.AnchorBottom)
    l.addAnchor(f, Qt.AnchorPoint.AnchorBottom, g, Qt.AnchorPoint.AnchorTop)
    l.addAnchor(c, Qt.AnchorPoint.AnchorBottom, g, Qt.AnchorPoint.AnchorBottom)

    # Horizontal.
    l.addAnchor(l, Qt.AnchorPoint.AnchorLeft, a, Qt.AnchorPoint.AnchorLeft)
    l.addAnchor(l, Qt.AnchorPoint.AnchorLeft, d, Qt.AnchorPoint.AnchorLeft)
    l.addAnchor(a, Qt.AnchorPoint.AnchorRight, b, Qt.AnchorPoint.AnchorLeft)

    l.addAnchor(a, Qt.AnchorPoint.AnchorRight, c, Qt.AnchorPoint.AnchorLeft)
    l.addAnchor(c, Qt.AnchorPoint.AnchorRight, e, Qt.AnchorPoint.AnchorLeft)

    l.addAnchor(b, Qt.AnchorPoint.AnchorRight, l, Qt.AnchorPoint.AnchorRight)
    l.addAnchor(e, Qt.AnchorPoint.AnchorRight, l, Qt.AnchorPoint.AnchorRight)
    l.addAnchor(d, Qt.AnchorPoint.AnchorRight, e, Qt.AnchorPoint.AnchorLeft)

    l.addAnchor(l, Qt.AnchorPoint.AnchorLeft, f, Qt.AnchorPoint.AnchorLeft)
    l.addAnchor(l, Qt.AnchorPoint.AnchorLeft, g, Qt.AnchorPoint.AnchorLeft)
    l.addAnchor(f, Qt.AnchorPoint.AnchorRight, g, Qt.AnchorPoint.AnchorRight)

    scene.addItem(w)
    scene.setBackgroundBrush(Qt.GlobalColor.darkGreen)

    view = QGraphicsView(scene)
    view.show()

    sys.exit(app.exec())
