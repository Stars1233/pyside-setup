// Copyright (C) 2025 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

import QtQuick
import QtQuick.Controls

SpinBox {
    id: root

    property int innerPadding: 10

    height: contentItem.implicitHeight + innerPadding
    width: contentItem.width + up.indicator.implicitWidth + down.indicator.implicitWidth

    background: Rectangle {
        border.color: Constants.secondaryColor
    }

    contentItem: Text {
        color: "black"
        height: parent.height
        horizontalAlignment: Text.AlignHCenter
        text: root.textFromValue(root.value, root.locale)
        verticalAlignment: Text.AlignVCenter
        width: implicitWidth + innerPadding * 2
    }

    down.indicator: Rectangle {
        border.color: Constants.secondaryColor
        color: root.down.pressed ? Constants.mediumGray : enabled ? Constants.darkGray : "black"
        height: parent.height
        implicitWidth: downText.implicitWidth + innerPadding * 2
        x: root.mirrored ? parent.width - width : 0

        Text {
            id: downText

            anchors.fill: parent
            color: "white"
            font.pixelSize: Math.round(root.font.pixelSize * 1.5)
            fontSizeMode: Text.Fit
            horizontalAlignment: Text.AlignHCenter
            text: "-"
            verticalAlignment: Text.AlignVCenter
        }
    }

    up.indicator: Rectangle {
        border.color: Constants.secondaryColor
        color: root.up.pressed ? Constants.mediumGray : enabled ? Constants.darkGray : "black"
        height: parent.height
        implicitWidth: upText.implicitWidth + innerPadding * 2
        x: root.mirrored ? 0 : parent.width - width

        Text {
            id: upText

            anchors.centerIn: parent
            anchors.fill: parent
            color: "white"
            font.pixelSize: Math.round(root.font.pixelSize * 1.5)
            fontSizeMode: Text.Fit
            horizontalAlignment: Text.AlignHCenter
            text: "+"
            verticalAlignment: Text.AlignVCenter
        }
    }
}
