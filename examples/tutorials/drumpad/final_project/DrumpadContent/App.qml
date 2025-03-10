// Copyright (C) 2026 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only

import QtQuick 2.15
import QtQuick.Window 2.15
import Drumpad 1.0

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
