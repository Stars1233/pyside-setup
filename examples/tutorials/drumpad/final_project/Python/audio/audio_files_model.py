# Copyright (C) 2025 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR BSD-3-Clause

from pathlib import Path

from PySide6.QtCore import QObject, Slot, QDirIterator
from PySide6.QtQml import QmlElement

from autogen.settings import project_root


QML_IMPORT_NAME = "Audio"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class AudioFilesModel(QObject):
    @Slot(result=list)
    def getModel(self):
        if "__compiled__" in globals():
            resource_prefix = ":/Sounds/"
            iterator = QDirIterator(resource_prefix, QDirIterator.Subdirectories)
            audio_files = []
            while iterator.hasNext():
                resource = iterator.next()
                audio_files.append(resource.split(resource_prefix)[-1])
            return audio_files

        return list(p.name for p in Path(project_root / "Sounds").glob("*.wav"))
