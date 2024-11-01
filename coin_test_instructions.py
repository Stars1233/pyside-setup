# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only
from __future__ import annotations

import logging
import os

from build_scripts.log import log
from build_scripts.utils import expand_clang_variables
from coin.instructions_utils import (CI, call_setup, get_architecture,
                                     get_python_version, remove_variables)

if __name__ == "__main__":
    ci = CI()
    log.setLevel(logging.INFO)
    # Remove some environment variables that impact cmake
    arch = get_architecture(ci)
    expand_clang_variables(arch)

    remove_variables(["CC", "CXX"])

    python_ver = get_python_version(ci)

    os.chdir(ci.ENV_AGENT_DIR)
    testRun = 0

    call_setup(python_ver, ci, "TEST", log)
