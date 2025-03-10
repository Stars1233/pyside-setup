// Copyright (C) 2025 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

import QtQuick
import QtQuick.Controls

Slider {
    id: root

    orientation: Qt.Vertical
    padding: 0

    background: Rectangle {
        color: Constants.mediumGray
        implicitHeight: root.height
        implicitWidth: root.width
        radius: width / 2

        Rectangle {
            anchors.bottom: parent.bottom
            anchors.horizontalCenter: parent.horizontalCenter
            color: Qt.lighter(Constants.primaryColor, 1 - (root.visualPosition * 0.3))
            height: (1 - root.visualPosition) * parent.height + (root.visualPosition * handle.height)
            radius: parent.width / 2
            width: parent.width
        }
    }

    handle: Rectangle {
        border.color: "#b0b0b0"
        border.width: 1
        color: root.pressed ? "#e0e0e0" : "#ffffff"
        height: root.width
        radius: width / 2
        width: root.width
        x: root.availableWidth / 2 - height / 2
        y: root.visualPosition * (root.availableHeight - height)
    }
}
