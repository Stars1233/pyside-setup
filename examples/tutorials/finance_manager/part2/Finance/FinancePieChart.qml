// Copyright (C) 2024 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

import QtQuick
import QtGraphs
import QtQuick.Controls.Material

Item {
    width: Screen.width
    height: Screen.height

    GraphsView {
        id: chart
        anchors.fill: parent
        antialiasing: true

        theme: GraphsTheme {
            colorScheme: Qt.Dark
            theme: GraphsTheme.Theme.QtGreenNeon
        }

        PieSeries {
            id: pieSeries
        }
    }

    Text {
        id: chartTitle
        text: "Total Expenses Breakdown by Category"
        color: "#5c8540"
        font.pixelSize: Qt.platform.os == "android" ?
            Math.min(window.width, window.height) * 0.04 :
            Math.min(window.width, window.height) * 0.03
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: parent.top
        anchors.topMargin: 20
    }

    function updateChart(data) {
        pieSeries.clear()
        for (var category in data) {
            var slice = pieSeries.append(category, data[category])
            slice.label = category + ": " + data[category] + "€"
            slice.labelVisible = true
        }
    }
}
