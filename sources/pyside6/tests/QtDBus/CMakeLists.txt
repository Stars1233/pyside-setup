# Copyright (C) 2023 The Qt Company Ltd.
# SPDX-License-Identifier: BSD-3-Clause

if(CMAKE_SYSTEM_NAME STREQUAL "Linux")
    PYSIDE_TEST(test_dbus.py)
endif()
