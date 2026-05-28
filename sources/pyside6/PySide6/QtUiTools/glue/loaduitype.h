// Copyright (C) 2026 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#ifndef LOADUITYPE_H
#define LOADUITYPE_H

#include <sbkpython.h>

#include <QtCore/qtclasshelpermacros.h>

QT_BEGIN_NAMESPACE

PyObject *loadUiType(PyObject *obFileName, PyObject *obPathSearch = nullptr);

QT_END_NAMESPACE

#endif // LOADUITYPE_H
