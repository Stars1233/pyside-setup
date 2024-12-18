# Copyright (C) 2024 The Qt Company Ltd.
# SPDX-License-Identifier: BSD-3-Clause

set(CMAKE_INCLUDE_CURRENT_DIR ON)

find_package(Qt6 REQUIRED COMPONENTS Core RemoteObjects)

add_executable(cpp_interop ${MOC_SOURCES} cpp_interop.cpp)
set_target_properties(cpp_interop PROPERTIES AUTOMOC ON)

target_link_libraries(cpp_interop PUBLIC
    Qt6::Core
    Qt6::RemoteObjects
)

# Add a custom target to build the C++ program
add_custom_target(build_cpp_interop
    COMMAND ${CMAKE_COMMAND} --build ${CMAKE_BINARY_DIR} --target cpp_interop
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
)

# Exclude windows (see cpp_interop.cpp)
if(NOT WIN32)
    PYSIDE_TEST(cpp_interop_test.py)
endif()