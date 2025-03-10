// Copyright (C) 2025 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

import QtQuick
import QtMultimedia

Item {
    id: root

    property double volume
    property url file

    MediaPlayer {
        id: player
        source: file
        audioOutput: AudioOutput {}
    }

    onVolumeChanged : {
        console.log("Mock: VolumeChanaged ", volume )
    }

    function play() {
        console.log("Mock: play()")
        player.play()
    }
}
