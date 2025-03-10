// Copyright (C) 2026 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only

import QtQuick

// A Flow layout that centers its children horizontally
// Note that the implementation adds unnecessary spacing in rows that are not full
Flow {
    property int customMargin: (children.length && (children[0].width + spacing <= parentWidth))
        ? (parentWidth - rowWidth) / 2 + padding
        : padding
    property int parentWidth: parent.width - 2 * padding
    property int rowCount: children.length ? parentWidth / (children[0].width + spacing) : 0
    property int rowWidth: children.length
        ? rowCount * children[0].width + (rowCount - 1) * spacing + 2 * padding
        : 0

    anchors {
        leftMargin: customMargin
        rightMargin: customMargin
    }
}
