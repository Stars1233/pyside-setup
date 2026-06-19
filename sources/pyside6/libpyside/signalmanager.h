// Copyright (C) 2016 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only
// Qt-Security score:significant reason:default

#ifndef SIGNALMANAGER_H
#define SIGNALMANAGER_H

#include "pysidemacros.h"

#include <sbkpython.h>
#include <shibokenmacros.h>

#include <QtCore/qmetaobject.h>

#include <optional>

namespace PySide
{

class PYSIDE_API SignalManager
{
public:
    Q_DISABLE_COPY_MOVE(SignalManager)
    ~SignalManager() = default;

    using QmlMetaCallErrorHandler = std::optional<int>(*)(QObject *object);

    static void init();

    static void setQmlMetaCallErrorHandler(QmlMetaCallErrorHandler handler);

    static bool emitSignal(QObject* source, const char* signal, PyObject* args);
    static bool emitSignal(QObject* source, int signalIndex, PyObject* args);
    static int qt_metacall(QObject* object, QMetaObject::Call call, int id, void** args);

    // Used to register a new signal/slot on QMetaobject of source.
    static bool registerMetaMethod(QObject* source, const char* signature,
                                   QMetaMethod::MethodType type);
    static int registerMetaMethodGetIndex(QObject* source, const char *signature,
                                          QMetaMethod::MethodType type);
    static int registerMetaMethodGetIndexBA(QObject* source, const QByteArray &signature,
                                            QMetaMethod::MethodType type);

    // used to discovery metaobject
    static const QMetaObject* retrieveMetaObject(PyObject* self);

    // Utility function to call a python method using args received in qt_metacall
    static int callPythonMetaMethod(QMetaMethod method, void **args, PyObject *callable);
    static int callPythonMetaMethod(const QByteArrayList &parameterTypes,
                                    const char *returnType /* = nullptr */,
                                    void **args, PyObject *callable);
    static void handleMetaCallError();
};

} // namespace PySide

#endif // SIGNALMANAGER_H
