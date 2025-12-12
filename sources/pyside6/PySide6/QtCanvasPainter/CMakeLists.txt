# Copyright (C) 2026 The Qt Company Ltd.
# SPDX-License-Identifier: BSD-3-Clause

project(QtCanvasPainter)

set (QtCanvasPainter_DROPPED_ENTRIES)

set(QtCanvasPainter_SRC
${QtCanvasPainter_GEN_DIR}/qcboxgradient_wrapper.cpp
${QtCanvasPainter_GEN_DIR}/qcboxshadow_wrapper.cpp
${QtCanvasPainter_GEN_DIR}/qcbrush_wrapper.cpp
${QtCanvasPainter_GEN_DIR}/qcconicalgradient_wrapper.cpp
${QtCanvasPainter_GEN_DIR}/qccustombrush_wrapper.cpp
${QtCanvasPainter_GEN_DIR}/qcgradient_wrapper.cpp
${QtCanvasPainter_GEN_DIR}/qcgridpattern_wrapper.cpp
${QtCanvasPainter_GEN_DIR}/qcimage_wrapper.cpp
${QtCanvasPainter_GEN_DIR}/qcimagepattern_wrapper.cpp
${QtCanvasPainter_GEN_DIR}/qclineargradient_wrapper.cpp
${QtCanvasPainter_GEN_DIR}/qcoffscreencanvas_wrapper.cpp
${QtCanvasPainter_GEN_DIR}/qcpainter_wrapper.cpp
${QtCanvasPainter_GEN_DIR}/qcpainterfactory_wrapper.cpp
${QtCanvasPainter_GEN_DIR}/qcpainterpath_wrapper.cpp
${QtCanvasPainter_GEN_DIR}/qcpainterwidget_wrapper.cpp
${QtCanvasPainter_GEN_DIR}/qcradialgradient_wrapper.cpp
${QtCanvasPainter_GEN_DIR}/qcrhipaintdriver_wrapper.cpp
${QtCanvasPainter_GEN_DIR}/qquickcpainteritem_wrapper.cpp
${QtCanvasPainter_GEN_DIR}/qquickcpainterrenderer_wrapper.cpp
# module is always needed
${QtCanvasPainter_GEN_DIR}/qtcanvaspainter_module_wrapper.cpp
)

set(QtGui_private_include_dirs
    ${Qt${QT_MAJOR_VERSION}Core_PRIVATE_INCLUDE_DIRS}
    ${Qt${QT_MAJOR_VERSION}Gui_PRIVATE_INCLUDE_DIRS})

configure_file("${QtCanvasPainter_SOURCE_DIR}/QtCanvasPainter_global.post.h.in"
               "${QtCanvasPainter_BINARY_DIR}/QtCanvasPainter_global.post.h" @ONLY)

set(QtCanvasPainter_include_dirs ${QtCanvasPainter_SOURCE_DIR}
                                  ${QtQml_SOURCE_DIR}
                                  ${Qt${QT_MAJOR_VERSION}Core_INCLUDE_DIRS}
                                  ${Qt${QT_MAJOR_VERSION}Gui_INCLUDE_DIRS}
                                  ${QtGui_private_include_dirs}
                                  ${Qt${QT_MAJOR_VERSION}Widgets_INCLUDE_DIRS}
                                  ${Qt${QT_MAJOR_VERSION}Network_INCLUDE_DIRS}
                                  ${Qt${QT_MAJOR_VERSION}Qml_INCLUDE_DIRS}
                                  ${Qt${QT_MAJOR_VERSION}Quick_INCLUDE_DIRS}
                                  ${Qt${QT_MAJOR_VERSION}CanvasPainter_INCLUDE_DIRS}
                                  ${libpyside_SOURCE_DIR}
                                  ${QtWidgets_GEN_DIR}
                                  ${QtGui_GEN_DIR}
                                  ${QtCore_GEN_DIR}
                                  ${QtNetwork_GEN_DIR}
                                  ${QtQml_GEN_DIR}
                                  ${QtQuick_GEN_DIR}
                                  ${QtCanvasPainter_GEN_DIR})

set(QtCanvasPainter_libraries pyside6
    ${Qt${QT_MAJOR_VERSION}CanvasPainter_LIBRARIES})

set(QtCanvasPainter_deps QtGui QtWidgets QtNetwork QtQml QtQuick)

check_qt_opengl("CanvasPainter" QtCanvasPainter_include_dirs QtCanvasPainter_deps
                QtCanvasPainter_DROPPED_ENTRIES)

create_pyside_module(NAME QtCanvasPainter
                     INCLUDE_DIRS QtCanvasPainter_include_dirs
                     LIBRARIES QtCanvasPainter_libraries
                     DEPS QtCanvasPainter_deps
                     TYPESYSTEM_PATH QtCanvasPainter_SOURCE_DIR
                     SOURCES QtCanvasPainter_SRC
                     DROPPED_ENTRIES QtCanvasPainter_DROPPED_ENTRIES
                     ADDITIONAL_INCLUDE_DIRS QtGui_private_include_dirs)
