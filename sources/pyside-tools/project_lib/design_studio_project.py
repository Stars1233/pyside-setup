# Copyright (C) 2024 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

from pathlib import Path


class DesignStudioProject:
    """
    Class to handle Design Studio projects. The project structure is as follows:
    - Python folder
        - autogen folder
            - settings.py
            - resources.py (Compiled resources)
        - main.py
    <ProjectName>.qrc (Resources collection file)
    <ProjectName>.qmlproject
    <ProjectName>.qmlproject.qtds
    ... Other files and folders ...
    """

    def __init__(self, main_file: Path):
        self.main_file = main_file
        self.project_dir = main_file.parent.parent
        self.compiled_resources_file = self.main_file.parent / "autogen" / "resources.py"

    @staticmethod
    def is_ds_project(main_file: Path) -> bool:
        return bool(*main_file.parent.parent.glob("*.qmlproject")) and bool(
            *main_file.parent.parent.glob("*.qmlproject.qtds")
        )

    def compiled_resources_available(self) -> bool:
        """
        Returns whether the resources of the project have been compiled into a .py file.
        TODO: Make the resources path configurable. Wait for the TOML configuration change
        """
        return self.compiled_resources_file.exists()
