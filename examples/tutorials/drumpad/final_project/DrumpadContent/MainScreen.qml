// Copyright (C) 2026 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Drumpad
import Audio

Rectangle {
    id: root

    property QtObject soundEffectPlayer: Qt.createComponent("../Drumpad/SoundEffectPlayer.qml",
                                                            Component.PreferSynchronous)

    color: "black"
    focus: true

    Component.onCompleted: {
        // Initialize the default sound effect players
        for (var i = 0; i < audioPlayersSpinBox.value; i++) {
            root.soundEffectPlayer.createObject(soundEffectPlayersFlow, {
                index: i
            });
        }
    }
    Keys.onPressed: event => {
        if (event.key < Qt.Key_1 || event.key > Qt.Key_9) {
            // Ignore key out of scope
            return;
        }

        let digit = event.key - Qt.Key_1;
        if (digit < soundEffectPlayersFlow.children.length) {
            soundEffectPlayersFlow.children[digit].play();
        }
    }

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 10

        Row {
            id: audioPlayersCountRow

            Layout.alignment: Qt.AlignHCenter
            spacing: 5

            Text {
                anchors.verticalCenter: parent.verticalCenter
                color: "white"
                text: "Audio players:"
            }

            StyledSpinBox {
                id: audioPlayersSpinBox

                value: 5

                onValueModified: {
                    let soundPlayersCount = soundEffectPlayersFlow.children.length;
                    if (audioPlayersSpinBox.value < soundPlayersCount) {
                        // Remove extra sound effect players
                        soundEffectPlayersFlow.children.length = audioPlayersSpinBox.value;
                        return;
                    }

                    if (audioPlayersSpinBox.value < soundPlayersCount) {
                        return;
                    }
                    // Create more sound effect players
                    for (var i = soundPlayersCount; i < audioPlayersSpinBox.value; i++) {
                        root.soundEffectPlayer.createObject(soundEffectPlayersFlow, {
                            index: i
                        });
                    }
                }
            }
        }

        ScrollView {
            Layout.fillHeight: true
            Layout.fillWidth: true
            contentWidth: width

            background: Rectangle {
                color: "#232323"
            }

            CenteredFlow {
                id: soundEffectPlayersFlow

                anchors.fill: parent
                padding: 10
                spacing: 10
            }
        }
    }
}
