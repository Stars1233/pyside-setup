// Copyright (C) 2024 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Controls.Material
import Finance

ApplicationWindow {
    id: window
    Material.theme: Material.Dark
    Material.accent: Material.Gray
    width: Screen.width * 0.3
    height: Screen.height * 0.5
    visible: true
    title: qsTr("Finance Manager")

    // Add a toolbar for the application, only visible on mobile
    header: ToolBar {
        Material.primary: "#5c8540"
        visible: Qt.platform.os == "android"
        RowLayout {
            anchors.fill: parent
            Label {
                text: qsTr("Finance Manager")
                font.pixelSize: 20
                Layout.alignment: Qt.AlignCenter
            }
        }
    }

    ColumnLayout {
        anchors.fill: parent

        TabBar {
            id: tabBar
            Layout.fillWidth: true

            TabButton {
                text: qsTr("Expenses")
                font.pixelSize: Qt.platform.os == "android" ?
                    Math.min(window.width, window.height) * 0.04 :
                    Math.min(window.width, window.height) * 0.02
                onClicked: stackView.currentIndex = 0
            }

            TabButton {
                text: qsTr("Charts")
                font.pixelSize: Qt.platform.os == "android" ?
                    Math.min(window.width, window.height) * 0.04 :
                    Math.min(window.width, window.height) * 0.02
                onClicked: stackView.currentIndex = 1
            }
        }

        StackLayout {
            id: stackView
            Layout.fillWidth: true
            Layout.fillHeight: true

            Item {
                id: expensesView
                Layout.fillWidth: true
                Layout.fillHeight: true

                FinanceView {
                    id: financeView
                    anchors.fill: parent
                    financeModel: finance_model
                }
            }

            Item {
                id: chartsView
                Layout.fillWidth: true
                Layout.fillHeight: true

                FinancePieChart {
                    id: financePieChart
                    anchors.fill: parent
                    Component.onCompleted: {
                        var categoryData = finance_model.getCategoryData()
                        updateChart(categoryData)
                    }
                }
            }
        }
    }

    // Model to store the finance data. Created from Python.
    FinanceModel {
        id: finance_model
    }

    // Add a dialog to add new entries
    AddDialog {
        id: addDialog
        onFinished: function(item_name, category, cost, date) {
            finance_model.append(item_name, category, cost, date)
            var categoryData = finance_model.getCategoryData()
            financePieChart.updateChart(categoryData)
        }
    }

    // Add a button to open the dialog
    ToolButton {
        id: roundButton
        text: qsTr("+")
        highlighted: true
        Material.elevation: 6
        width: Qt.platform.os === "android" ?
            Math.min(parent.width * 0.2, Screen.width * 0.15) :
            Math.min(parent.width * 0.060, Screen.width * 0.05)
        height: width  // Keep the button circular
        anchors.margins: 10
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        background: Rectangle {
            color: "#5c8540"
            radius: roundButton.width / 2
        }
        font.pixelSize: width * 0.4
        onClicked: {
            addDialog.createEntry()
        }
    }
}
