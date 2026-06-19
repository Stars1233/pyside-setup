// Copyright (C) 2026 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only
// Qt-Security score:critical reason:handling-untrusted-data

#include "pyobjectwrapper.h"
#include "pysideglobals_p.h"

#include <autodecref.h>
#include <basewrapper.h>
#include <gilstate.h>
#include <sbkenum.h>
#include <sbkpep.h>
#include <sbkstring.h>
#include <sbkstaticstrings.h>

#include <QtCore/qdebug.h>

using namespace Qt::StringLiterals;

static int pyObjectWrapperMetaTypeId = QMetaType::UnknownType;

namespace PySide {

PyObjectWrapper::PyObjectWrapper()
    :m_me(Py_None)
{
    // PYSIDE-813: When PYSIDE-164 was solved by adding some thread allowance,
    // this code was no longer protected. It was hard to find this connection.
    // See PYSIDE-813 for details.
    Shiboken::GilState gil;
    Py_XINCREF(m_me);
}

PyObjectWrapper::PyObjectWrapper(PyObject *me)
    : m_me(me)
{
    Shiboken::GilState gil;
    Py_XINCREF(m_me);
}

PyObjectWrapper::PyObjectWrapper(const PyObjectWrapper &other)
    : m_me(other.m_me)
{
    Shiboken::GilState gil;
    Py_XINCREF(m_me);
}

PyObjectWrapper::PyObjectWrapper(PyObjectWrapper &&other) noexcept
 : m_me{std::exchange(other.m_me, nullptr)}
{
}

PyObjectWrapper &PyObjectWrapper::operator=(PyObjectWrapper &&other) noexcept
{
    m_me = std::exchange(other.m_me, nullptr);
    return *this;
}

PyObjectWrapper::~PyObjectWrapper()
{
    // Check that Python is still initialized as sometimes this is called by a static destructor
    // after Python interpeter is shutdown.
    if (!Py_IsInitialized())
        return;

    Shiboken::GilState gil;
    Py_XDECREF(m_me);
}

void PyObjectWrapper::reset(PyObject *o)
{
    Shiboken::GilState gil;
    Py_XINCREF(o);
    Py_XDECREF(m_me);
    m_me = o;
}

PyObjectWrapper &PyObjectWrapper::operator=(const PySide::PyObjectWrapper &other)
{
    if (this != &other)
        reset(other.m_me);
    return *this;
}

PyObjectWrapper::operator PyObject *() const
{
    return m_me;
}

int PyObjectWrapper::metaTypeId()
{
    return pyObjectWrapperMetaTypeId;
}

void PyObjectWrapper::registerMetaType()
{
    // Register PyObject type to use in queued signal and slot connections
    pyObjectWrapperMetaTypeId = qRegisterMetaType<PyObjectWrapper>("PyObject");
}

int PyObjectWrapper::toInt() const
{
    // hold the GIL
    Shiboken::GilState state;
    return Shiboken::Enum::check(m_me) ? Shiboken::Enum::getValue(m_me) : -1;
}

QDataStream &operator<<(QDataStream &out, const PyObjectWrapper &myObj)
{
    if (Py_IsInitialized() == 0) {
        qWarning("libpyside: Stream operator for PyObject called without python interpreter.");
        return out;
    }

    PyObject *&reduce_func = PySide::globals()->pickleReduceFunc;

    Shiboken::GilState gil;
    if (!reduce_func) {
        Shiboken::AutoDecRef pickleModule(PyImport_ImportModule("pickle"));
        reduce_func = PyObject_GetAttr(pickleModule, Shiboken::PyName::dumps());
    }
    PyObject *pyObj = myObj;
    Shiboken::AutoDecRef repr(PyObject_CallFunctionObjArgs(reduce_func, pyObj, nullptr));
    if (repr.object()) {
        const char *buff = nullptr;
        Py_ssize_t size  = 0;
        if (PyBytes_Check(repr.object())) {
            buff = PyBytes_AsString(repr.object());
            size = PyBytes_Size(repr.object());
        } else if (Shiboken::String::check(repr.object())) {
            buff = Shiboken::String::toCString(repr.object());
            size = Shiboken::String::len(repr.object());
        }
        QByteArray data(buff, size);
        out << data;
    }
    return out;
}

QDataStream &operator>>(QDataStream &in, PyObjectWrapper &myObj)
{
    if (Py_IsInitialized() == 0) {
        qWarning("libpyside: Stream operator for PyObject called without python interpreter.");
        return in;
    }

    PyObject *&eval_func = PySide::globals()->pickleEvalFunc;

    Shiboken::GilState gil;
    if (!eval_func) {
        Shiboken::AutoDecRef pickleModule(PyImport_ImportModule("pickle"));
        eval_func = PyObject_GetAttr(pickleModule, Shiboken::PyName::loads());
    }

    QByteArray repr;
    in >> repr;
    Shiboken::AutoDecRef pyCode(PyBytes_FromStringAndSize(repr.data(), repr.size()));
    Shiboken::AutoDecRef value(PyObject_CallFunctionObjArgs(eval_func, pyCode.object(), 0));
    if (!value.object())
        value.reset(Py_None);
    myObj.reset(value);
    return in;
}

PYSIDE_API QDebug operator<<(QDebug debug, const PyObjectWrapper &myObj)
{
    QDebugStateSaver saver(debug);
    debug.noquote();
    debug.nospace();
    // Do not repeat the type name as it is typically called from the QVariant debug
    // operator, which outputs the type.
    debug << '<';
    if (PyObject *ob = myObj) {
        const auto refs = Py_REFCNT(ob);
        debug << PepType_GetFullyQualifiedNameStr(Py_TYPE(ob)) << " at " << ob;
        if (refs == UINT_MAX) // _Py_IMMORTAL_REFCNT
            debug << ", immortal";
        else
            debug << ", refs=" << refs;
    } else {
        debug << '0';
    }
    debug << '>';
    return debug;
}

} // namespace PySide
