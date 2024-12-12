// Copyright (C) 2024 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

import QtQuick
import Drumpad

Window {
    id: root

    height: 800
    title: "Drumpad"
    visible: true
    width: 1200

    MainScreen {
        id: mainScreen

        anchors.fill: parent
    }
}
