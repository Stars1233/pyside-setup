// Copyright (C) 2024 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Dialog {
    id: dialog

    signal finished(string itemName, string category, real cost, string date)

    contentItem: ColumnLayout {
        id: form
        spacing: 10
        property alias itemName: itemName
        property alias category: category
        property alias cost: cost
        property alias date: date

        GridLayout {
            columns: 2
            columnSpacing: 20
            rowSpacing: 10
            Layout.fillWidth: true

            Label {
                text: qsTr("Item Name:")
                Layout.alignment: Qt.AlignLeft | Qt.AlignBaseline
            }

            TextField {
                id: itemName
                focus: true
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignLeft | Qt.AlignBaseline
            }

            Label {
                text: qsTr("Category:")
                Layout.alignment: Qt.AlignLeft | Qt.AlignBaseline
            }

            TextField {
                id: category
                focus: true
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignLeft | Qt.AlignBaseline
            }

            Label {
                text: qsTr("Cost:")
                Layout.alignment: Qt.AlignLeft | Qt.AlignBaseline
            }

            TextField {
                id: cost
                focus: true
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignLeft | Qt.AlignBaseline
                placeholderText: qsTr("€")
                inputMethodHints: Qt.ImhFormattedNumbersOnly
            }

            Label {
                text: qsTr("Date:")
                Layout.alignment: Qt.AlignLeft | Qt.AlignBaseline
            }

            TextField {
                id: date
                Layout.fillWidth: true
                Layout.alignment: Qt.AlignLeft | Qt.AlignBaseline
                // placeholderText: qsTr("dd-mm-yyyy")
                validator: RegularExpressionValidator { regularExpression: /^[0-3]?\d-[01]?\d-\d{4}$/ }
                // code to add the - automatically
                onTextChanged: {
                    if (date.text.length === 2 || date.text.length === 5) {
                        date.text += "-"
                    }
                }
                Component.onCompleted: {
                var today = new Date();
                var day = String(today.getDate()).padStart(2, '0');
                var month = String(today.getMonth() + 1).padStart(2, '0'); // Months are zero-based
                var year = today.getFullYear();
                date.placeholderText = day + "-" + month + "-" + year;
                }
            }
        }
    }

    function createEntry() {
        form.itemName.clear()
        form.category.clear()
        form.cost.clear()
        form.date.clear()
        dialog.title = qsTr("Add Finance Item")
        dialog.open()
    }

    x: parent.width / 2 - width / 2
    y: parent.height / 2 - height / 2

    focus: true
    modal: true
    title: qsTr("Add Finance Item")
    standardButtons: Dialog.Ok | Dialog.Cancel

    Component.onCompleted: {
        dialog.visible = false
        Qt.inputMethod.visibleChanged.connect(adjustDialogPosition)
    }

    function adjustDialogPosition() {
        if (Qt.inputMethod.visible) {
            // If the keyboard is visible, move the dialog up
            dialog.y = parent.height / 4 - height / 2
        } else {
            // If the keyboard is not visible, center the dialog
            dialog.y = parent.height / 2 - height / 2
        }
    }

    onAccepted: {
        finished(form.itemName.text, form.category.text, parseFloat(form.cost.text), form.date.text)
    }
}
