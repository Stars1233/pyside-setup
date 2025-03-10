# Copyright (C) 2025 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

from PySide6.QtQml import QmlElement
from PySide6.QtCore import QObject, Slot, Property, Signal, QUrl
from PySide6.QtMultimedia import QSoundEffect

from autogen.settings import project_root

QML_IMPORT_NAME = "Audio"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class AudioEngine(QObject):
    volumeChanged = Signal()
    fileChanged = Signal()
    isPlayingChanged = Signal()
    decodingStatusChanged = Signal(QSoundEffect.Status, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._sound_effect = QSoundEffect()
        self._sound_effect.playingChanged.connect(self.isPlayingChanged.emit)  #
        self._sound_effect.statusChanged.connect(self.reportStatus)

    def reportStatus(self):
        if self._sound_effect.status() == QSoundEffect.Status.Error:
            self.decodingStatusChanged.emit(
                QSoundEffect.Status.Error,
                f"Error decoding file: {self._sound_effect.source().path()}",
            )
        else:
            self.decodingStatusChanged.emit(self._sound_effect.status(), "")

    @Slot(result=None)
    def play(self):
        self._sound_effect.play()

    def volume(self):
        return self._sound_effect.volume()

    def setVolume(self, value):
        self._sound_effect.setVolume(value)
        self.volumeChanged.emit()

    def file(self):
        return self._sound_effect.source()

    def setFile(self, value: QUrl):
        if self._sound_effect.source() == value or value.isEmpty():
            return

        if "__compiled__" in globals():
            self._sound_effect.setSource(f"qrc:/{value.toString()}")
        else:
            self._sound_effect.setSource(f"file:{project_root / value.toString()}")
        self.fileChanged.emit()

    def isPlaying(self):
        return self._sound_effect.isPlaying()

    volume = Property(float, volume, setVolume, notify=volumeChanged)
    file = Property(QUrl, file, setFile, notify=fileChanged)
    isPlaying = Property(bool, isPlaying, notify=isPlayingChanged)
