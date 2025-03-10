# Copyright (C) 2025 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

import struct

from PySide6.QtCore import Qt, Property, QUrl, Signal, QFile, QPointF
from PySide6.QtGui import QPen, QPainter
from PySide6.QtMultimedia import QAudioFormat, QAudioDecoder
from PySide6.QtQml import QmlElement
from PySide6.QtQuick import QQuickPaintedItem

QML_IMPORT_NAME = "Audio"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class WaveformItem(QQuickPaintedItem):

    fileChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._waveformData = []
        self._background_color = Qt.black

        audio_format = QAudioFormat()
        audio_format.setChannelCount(1)
        audio_format.setSampleRate(44100)
        audio_format.setSampleFormat(QAudioFormat.Float)

        self._file_url: QUrl | None = None
        self._audio_file: QFile | None = None

        self._decoder = QAudioDecoder()
        self._decoder.setAudioFormat(audio_format)

        self._decoder.bufferReady.connect(self.onBufferReady)
        self._decoder.finished.connect(self.decoderFinished)

    def file(self) -> QUrl | None:
        return self._file_url

    def setFile(self, value: QUrl):
        if self._decoder.source() == value:
            return

        if self._audio_file and self._audio_file.isOpen():
            self._audio_file.close()

        self._waveformData = []
        self._decoder.stop()

        self._file_url = value
        if "__compiled__" in globals():
            path = self._file_url.toString().replace("qrc:/", ":/")
        else:
            path = self._file_url.path()
        self._audio_file = QFile(path)
        self._audio_file.open(QFile.ReadOnly)
        self._decoder.setSourceDevice(self._audio_file)
        self._decoder.start()
        self.fileChanged.emit()

    def paint(self, painter):
        # Fill the bounding rectangle with the specified color
        painter.fillRect(self.boundingRect(), self._background_color)

        # If no waveform data is available, draw the text
        if not self._waveformData:
            painter.setPen(Qt.white)
            painter.drawText(self.boundingRect(), Qt.AlignCenter, "Waveform not available")
            return

        painter.setRenderHint(QPainter.Antialiasing)

        # Set the pen for drawing the waveform
        pen = QPen(Qt.blue)
        pen.setWidth(1)
        painter.setPen(pen)

        # Get container dimensions
        rect = self.boundingRect()
        data_size = len(self._waveformData)

        # Calculate step size and center line
        x_step = rect.width() / data_size
        center_y = rect.height() / 2.0

        # Draw the waveform as connected lines
        for i in range(1, data_size):
            x1 = (i - 1) * x_step
            y1 = center_y - self._waveformData[i - 1] * center_y
            x2 = i * x_step
            y2 = center_y - self._waveformData[i] * center_y
            painter.drawLine(QPointF(x1, y1), QPointF(x2, y2))

    @staticmethod
    def float_buffer_to_list(data):
        # Calculate the number of 32-bit floats in the buffer
        float_count = len(data) // 4  # Each float32 is 4 bytes
        # Unpack the binary data into a list of floats
        return list(struct.unpack(f"{float_count}f", data))

    def onBufferReady(self):
        buffer = self._decoder.read()
        data = buffer.constData()
        self._waveformData.extend(self.float_buffer_to_list(data))
        self.update()

    file: QUrl = Property(QUrl, file, setFile, notify=fileChanged)

    def decoderFinished(self):
        self._audio_file.close()
