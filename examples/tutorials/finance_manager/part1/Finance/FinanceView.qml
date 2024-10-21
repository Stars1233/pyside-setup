// Copyright (C) 2024 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material

ListView {
    id: listView
    anchors.fill: parent
    height: parent.height
    property var financeModel

    delegate: FinanceDelegate {
        id: delegate
        width: listView.width
    }

    model: financeModel

    section.property: "month"  // Group items by the "month" property
    section.criteria: ViewSection.FullString
    section.delegate: Component {
        id: sectionHeading
        Rectangle {
            width: listView.width
            height:  Qt.platform.os == "android" ?
                Math.min(window.width, window.height) * 0.05 :
                Math.min(window.width, window.height) * 0.03
            color: "#5c8540"

            required property string section

            Text {
                text: parent.section
                font.bold: true
                // depending on the screen density, adjust the font size
                font.pixelSize: Qt.platform.os == "android" ?
                    Math.min(window.width, window.height) * 0.03 :
                    Math.min(window.width, window.height) * 0.02
                color: Material.primaryTextColor
            }
        }
    }

    ScrollBar.vertical: ScrollBar { }
}
