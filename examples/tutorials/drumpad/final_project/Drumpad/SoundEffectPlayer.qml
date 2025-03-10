// Copyright (C) 2026 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only

import QtQuick
import QtQuick.Layouts
import QtQuick.Dialogs
import QtMultimedia

import Drumpad
import Audio

Rectangle {
    id: root

    property string decodingError: ""
    required property int index
    property int status: SoundEffect.Null
    property bool isLoading: status == SoundEffect.Loading
    property bool isError: status == SoundEffect.Error || status == SoundEffect.Null
    property bool isReady: status == SoundEffect.Ready

    function play() {
        if (root.status == SoundEffect.Ready) {
            audioEngine.play();
        }
    }

    color: Constants.darkGray
    implicitHeight: layout.implicitHeight + 2 * layout.anchors.margins
    implicitWidth: layout.implicitWidth + 2 * layout.anchors.margins
    radius: 10

    onDecodingErrorChanged: {
        if (status == SoundEffect.Error && root.decodingError) {
            errorMessageDialog.text = root.decodingError;
            errorMessageDialog.open();
        }
    }

    AudioEngine {
        id: audioEngine

        file: availableSoundsComboBox.currentFile
        volume: volumeSlider.value

        onDecodingStatusChanged: (status, error) => {
            root.status = status;
            if (status == SoundEffect.Error && error) {
                root.decodingError = error;
            } else {
                root.decodingError = "";
            }
        }
    }

    MessageDialog {
        id: errorMessageDialog

        buttons: MessageDialog.Ok
        title: "Error decoding file"
    }

    ColumnLayout {
        id: layout

        anchors.fill: parent
        anchors.margins: 10
        spacing: 10

        RowLayout {
            spacing: 10

            Text {
                Layout.alignment: Qt.AlignVCenter
                Layout.fillWidth: true
                color: "white"
                text: `Player ${root.index + 1}`
            }
            AvailableSoundsComboBox {
                id: availableSoundsComboBox

                Layout.alignment: Qt.AlignCenter
                initialIndex: root.index
            }
        }

        WaveformItem {
            id: waveformItem

            file: audioEngine.file
            height: 100
            width: 300
        }

        Row {
            Layout.alignment: Qt.AlignCenter
            spacing: 10

            PadButton {
                id: padRectangle
                height: 100
                width: 100
                isPlaying: audioEngine.isPlaying
                isError: root.isError
                isLoading: root.isLoading
                onPressed: root.play()
            }

            VolumeSlider {
                id: volumeSlider

                height: padRectangle.height
                value: 0.75
                width: 16
            }
        }
    }
}
