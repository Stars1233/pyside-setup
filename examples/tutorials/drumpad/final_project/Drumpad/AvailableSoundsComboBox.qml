// Copyright (C) 2026 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only

pragma ComponentBehavior: Bound
import QtQuick
import QtQuick.Controls
import Audio

ComboBox {
    id: root

    property string currentFile: currentText ? `Sounds/${currentText}` : ""
    required property int initialIndex

    model: audioFilesModel.getModel()

    background: Rectangle {
        border.color: root.pressed ? Constants.primaryColor : Constants.secondaryColor
        border.width: root.visualFocus ? 3 : 2
        color: root.pressed ? Constants.secondaryColor : "black"
        implicitHeight: 30
        radius: 2
    }
    contentItem: Text {
        color: "white"
        elide: Text.ElideRight
        leftPadding: 10
        rightPadding: root.indicator.width + 10
        text: root.displayText
        verticalAlignment: Text.AlignVCenter
    }
    delegate: ItemDelegate {
        id: delegate

        required property int index

        highlighted: root.highlightedIndex === index

        background: Rectangle {
            color: delegate.highlighted ? Constants.darkGray : "black"
            implicitWidth: delegate.contentItem.implicitWidth
            width: popup.width
        }
        contentItem: Text {
            anchors.fill: parent
            color: delegate.highlighted ? "#ff0000" : "white"
            elide: Text.ElideRight
            leftPadding: 10
            text: root.model[delegate.index]
            verticalAlignment: Text.AlignVCenter
        }
    }
    indicator: Canvas {
        id: canvas

        contextType: "2d"
        height: 8
        width: 12
        x: root.width - canvas.width - root.rightPadding
        y: root.topPadding + (root.availableHeight - canvas.height) / 2

        onPaint: {
            let margin = 2;
            context.reset();
            context.lineWidth = 2;
            context.strokeStyle = "white";
            context.lineCap = "round";
            context.beginPath();
            context.moveTo(margin, margin);
            context.lineTo(width / 2, height - margin);
            context.lineTo(width - margin, margin);
            context.stroke();
        }

        Connections {
            function onPressedChanged() {
                canvas.requestPaint();
            }

            target: root
        }
    }
    popup: Popup {
        id: popup

        implicitHeight: contentItem.implicitHeight
        implicitWidth: 200
        padding: 2
        y: root.height + 2

        background: Rectangle {
            border.color: Constants.primaryColor
            border.width: 2
            color: "black"
        }
        contentItem: ListView {
            clip: true
            currentIndex: root.highlightedIndex
            implicitHeight: Math.min(contentHeight, 200)
            model: popup.visible ? root.delegateModel : null
        }
    }

    Component.onCompleted: {
        currentIndex = root.initialIndex % model.length;
    }

    AudioFilesModel {
        id: audioFilesModel
    }
}
