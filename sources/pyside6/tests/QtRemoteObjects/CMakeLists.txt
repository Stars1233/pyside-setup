# Copyright (C) 2025 Ford Motor Company
# SPDX-License-Identifier: BSD-3-Clause

# FIXME:  TypeError: Failed to generate default value. Error: name 'int' is not defined. Problematic code: int(2)
if(NOT APPLE)
PYSIDE_TEST(repfile_test.py)
PYSIDE_TEST(dynamic_types_test.py)
PYSIDE_TEST(integration_test.py)

add_subdirectory(cpp_interop)
endif()
