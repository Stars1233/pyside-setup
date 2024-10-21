// Copyright (C) 2024 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

import QtQuick
import QtQuick.Layouts
import QtQuick.Controls
import QtQuick.Controls.Material

ItemDelegate {
    id: delegate
    checkable: true
    width: parent.width
    height: Qt.platform.os == "android" ?
        Math.min(window.width, window.height) * 0.15 :
        Math.min(window.width, window.height) * 0.1

    contentItem:
    RowLayout {
        Label {
            id: dateLabel
            font.pixelSize: Qt.platform.os == "android" ?
                Math.min(window.width, window.height) * 0.03 :
                Math.min(window.width, window.height) * 0.02
            text: date
            elide: Text.ElideRight
            Layout.fillWidth: true
            Layout.preferredWidth: 1
            color: Material.primaryTextColor
        }

        ColumnLayout {
            spacing: 5
            Layout.fillWidth: true
            Layout.preferredWidth: 1

            Label {
                text: item_name
                color: "#5c8540"
                font.bold: true
                elide: Text.ElideRight
                font.pixelSize:  Qt.platform.os == "android" ?
                    Math.min(window.width, window.height) * 0.03 :
                    Math.min(window.width, window.height) * 0.02
                Layout.fillWidth: true
            }

            Label {
                text: category
                elide: Text.ElideRight
                Layout.fillWidth: true
                font.pixelSize:  Qt.platform.os == "android" ?
                    Math.min(window.width, window.height) * 0.03 :
                    Math.min(window.width, window.height) * 0.02
            }
        }

        Item {
        Layout.fillWidth: true  // This item will take up the remaining space
        }

        ColumnLayout {
            spacing: 5
            Layout.fillWidth: true
            Layout.preferredWidth: 1

            Label {
                text: "you spent:"
                color: "#5c8540"
                elide: Text.ElideRight
                Layout.fillWidth: true
                font.pixelSize:  Qt.platform.os == "android" ?
                    Math.min(window.width, window.height) * 0.03 :
                    Math.min(window.width, window.height) * 0.02
            }

            Label {
                text: cost + "€"
                elide: Text.ElideRight
                Layout.fillWidth: true
                font.pixelSize:  Qt.platform.os == "android" ?
                    Math.min(window.width, window.height) * 0.03 :
                    Math.min(window.width, window.height) * 0.02
            }
        }
    }
}
