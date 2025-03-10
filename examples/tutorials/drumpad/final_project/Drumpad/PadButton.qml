// Copyright (C) 2026 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only

import QtQuick
import QtQuick.Shapes

Rectangle {
    id: root

    property bool isPlaying: false
    property bool isError: false
    property bool isLoading: false
    property int cornerRadius: 10
    signal pressed()

    color: "transparent"

    Shape {
        anchors.fill: parent

        ShapePath {
            strokeColor: "black"
            strokeWidth: 2

            fillGradient: RadialGradient {
                centerRadius: root.height
                centerX: root.width / 2
                centerY: root.height / 2
                focalX: centerX
                focalY: centerY

                GradientStop {
                    position: 0
                    color: {
                        if (isError)
                            return "black";
                        if (isLoading)
                            return "yellow";
                        if (isPlaying)
                            return Qt.darker(Constants.primaryColor, 1.25);
                        return Qt.darker(Constants.secondaryColor, 1.25);
                    }
                }
                GradientStop {
                    position: 0.5
                    color: {
                        if (isError)
                            return Constants.darkGray;
                        if (isLoading)
                            return "orange";
                        if (isPlaying)
                            return Constants.primaryColor;
                        return Constants.secondaryColor;
                    }
                }
            }

            // Rounded shape path
            PathMove {
                x: root.cornerRadius
                y: 0
            }
            PathQuad {
                controlX: 0
                controlY: 0
                x: 0
                y: root.cornerRadius
            }
            PathLine {
                x: 0
                y: root.height - root.cornerRadius
            }
            PathQuad {
                controlX: 0
                controlY: root.height
                x: root.cornerRadius
                y: root.height
            }
            PathLine {
                x: root.width - root.cornerRadius
                y: root.height
            }
            PathQuad {
                controlX: root.width
                controlY: root.height
                x: root.width
                y: root.height - root.cornerRadius
            }
            PathLine {
                x: root.width
                y: root.cornerRadius
            }
            PathQuad {
                controlX: root.width
                controlY: 0
                x: root.width - root.cornerRadius
                y: 0
            }
            PathLine {
                x: root.cornerRadius
                y: 0
            }
        }
    }

    MouseArea {
        anchors.fill: parent
        onClicked: root.pressed()
    }
}
