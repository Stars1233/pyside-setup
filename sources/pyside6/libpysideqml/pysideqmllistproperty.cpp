// Copyright (C) 2021 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "pysideqmllistproperty_p.h"
#include "pysideqmlregistertype_p.h"

#include <autodecref.h>
#include <gilstate.h>
#include <pep384ext.h>
#include <sbkconverter.h>
#include <signature.h>
#include <sbkpep.h>
#include <sbkstring.h>
#include <sbktypefactory.h>

#include <pysideproperty.h>
#include <pysideproperty_p.h>
#include <pysideqobject.h>

#include <QtCore/qobject.h>
#include <QtQml/qqmllist.h>

// This is the user data we store in the property.
class QmlListPropertyPrivate : public PySidePropertyPrivate
{
public:
    void metaCall(PyObject *source, QMetaObject::Call call, void **args) override;

    PyTypeObject *type = nullptr;
    PyObject *append = nullptr;
    PyObject *count = nullptr;
    PyObject *at = nullptr;
    PyObject *clear = nullptr;
    PyObject *replace = nullptr;
    PyObject *removeLast = nullptr;
};

extern "C"
{

static PyObject *propList_tp_new(PyTypeObject *subtype, PyObject * /* args */, PyObject * /* kwds */)
{
    auto *me = PepExt_TypeCallAlloc<PySideProperty>(subtype, 0);
    me->d = new QmlListPropertyPrivate;
    return reinterpret_cast<PyObject *>(me);
}

static int propListTpInit(PyObject *self, PyObject *args, PyObject *kwds)
{
    static const char *kwlist[] = {"type", "append", "count", "at", "clear",
                                   "replace", "removeLast",
                                   "doc", "notify", // PySideProperty
                                   "designable", "scriptable", "stored",
                                   "user", "constant", "final",
                                   nullptr};
    auto *pySelf = reinterpret_cast<PySideProperty *>(self);

    auto *data = static_cast<QmlListPropertyPrivate *>(pySelf->d);

    char *doc{};
    PyObject *append{}, *count{}, *at{}, *clear{}, *replace{}, *removeLast{}, *notify{};
    bool designable{true}, scriptable{true}, stored{true};
    bool user{false}, constant{false}, finalProp{false};

    if (!PyArg_ParseTupleAndKeywords(args, kwds,
                                     "O|OOOOOOsObbbbbb:QtQml.ListProperty",
                                     const_cast<char **>(kwlist),
                                     &data->type,
                                     &append, &count, &at, &clear, &replace, &removeLast,
                                     /*s*/   &doc,
                                     /*O*/   &notify, // PySideProperty
                                     /*bbb*/ &designable, &scriptable, &stored,
                                     /*bbb*/ &user, &constant, &finalProp)) {
        return -1;
    }

    if (!PySidePropertyPrivate::assignCheckCallable(append, "append", &data->append)
        || !PySidePropertyPrivate::assignCheckCallable(count, "count", &data->count)
        || !PySidePropertyPrivate::assignCheckCallable(at, "at", &data->at)
        || !PySidePropertyPrivate::assignCheckCallable(clear, "clear", &data->clear)
        || !PySidePropertyPrivate::assignCheckCallable(replace, "replace", &data->replace)
        || !PySidePropertyPrivate::assignCheckCallable(removeLast, "removeLast", &data->removeLast)) {
        return -1;
    }

    if (notify != nullptr && notify != Py_None)
        data->notify = notify;

    if (doc)
        data->doc = doc;
    else
        data->doc.clear();

    PyTypeObject *qobjectType = PySide::qObjectType();

    if (!PySequence_Contains(data->type->tp_mro, reinterpret_cast<PyObject *>(qobjectType))) {
        PyErr_Format(PyExc_TypeError, "A type inherited from %s expected, got %s.",
                     qobjectType->tp_name, data->type->tp_name);
        return -1;
    }

    data->typeName = QByteArrayLiteral("QQmlListProperty<QObject>");

    auto &flags = data->flags;
    flags.setFlag(PySide::Property::PropertyFlag::Readable, true);
    flags.setFlag(PySide::Property::PropertyFlag::Designable, designable);
    flags.setFlag(PySide::Property::PropertyFlag::Scriptable, scriptable);
    flags.setFlag(PySide::Property::PropertyFlag::Stored, stored);
    flags.setFlag(PySide::Property::PropertyFlag::User, user);
    flags.setFlag(PySide::Property::PropertyFlag::Constant, constant);
    flags.setFlag(PySide::Property::PropertyFlag::Final, finalProp);

    return 0;
}

static PyTypeObject *createPropertyListType()
{
    PyType_Slot PropertyListType_slots[] = {
        {Py_tp_new, reinterpret_cast<void *>(propList_tp_new)},
        {Py_tp_init, reinterpret_cast<void *>(propListTpInit)},
        {0, nullptr}
    };

    PyType_Spec PropertyListType_spec = {
        "2:PySide6.QtQml.ListProperty",
        sizeof(PySideProperty),
        0,
        Py_TPFLAGS_DEFAULT,
        PropertyListType_slots,
    };

    Shiboken::AutoDecRef bases(Py_BuildValue("(O)", PySideProperty_TypeF()));
    return SbkType_FromSpecWithBases(&PropertyListType_spec, bases.object());
}

PyTypeObject *PropertyList_TypeF(void)
{
    // PYSIDE-2230: This was a wrong replacement by static AutoDecref.
    //              Never do that, deletes things way too late.
    static PyTypeObject *type = createPropertyListType();
    return type;
}

} // extern "C"

// Implementation of QQmlListProperty<T>::AppendFunction callback
void propListAppender(QQmlListProperty<QObject> *propList, QObject *item)
{
    Shiboken::GilState state;

    Shiboken::AutoDecRef args(PyTuple_New(2));
    PyTypeObject *qobjectType = PySide::qObjectType();
    PyTuple_SetItem(args, 0,
                     Shiboken::Conversions::pointerToPython(qobjectType, propList->object));
    PyTuple_SetItem(args, 1,
                     Shiboken::Conversions::pointerToPython(qobjectType, item));

    auto *data = reinterpret_cast<QmlListPropertyPrivate *>(propList->data);
    Shiboken::AutoDecRef retVal(PyObject_CallObject(data->append, args));

    if (PyErr_Occurred())
        PyErr_Print();
}

// Implementation of QQmlListProperty<T>::CountFunction callback
qsizetype propListCount(QQmlListProperty<QObject> *propList)
{
    Shiboken::GilState state;

    Shiboken::AutoDecRef args(PyTuple_New(1));
    auto *qobjType = PySide::qObjectType();
    PyTuple_SetItem(args, 0,
                     Shiboken::Conversions::pointerToPython(qobjType, propList->object));

    auto *data = reinterpret_cast<QmlListPropertyPrivate *>(propList->data);
    Shiboken::AutoDecRef retVal(PyObject_CallObject(data->count, args));

    // Check return type
    if (PyErr_Occurred()) {
        PyErr_Print();
        return 0;
    }

    qsizetype cppResult = 0;
    auto *converter = Shiboken::Conversions::PrimitiveTypeConverter<qsizetype>();
    if (auto *pythonToCpp = Shiboken::Conversions::isPythonToCppConvertible(converter, retVal))
        pythonToCpp(retVal, &cppResult);
    return cppResult;
}

// Implementation of QQmlListProperty<T>::AtFunction callback
QObject *propListAt(QQmlListProperty<QObject> *propList, qsizetype index)
{
    Shiboken::GilState state;

    Shiboken::AutoDecRef args(PyTuple_New(2));
    PyTypeObject *qobjectType = PySide::qObjectType();
    PyTuple_SetItem(args, 0,
                     Shiboken::Conversions::pointerToPython(qobjectType, propList->object));
    auto *converter = Shiboken::Conversions::PrimitiveTypeConverter<qsizetype>();
    PyTuple_SetItem(args, 1,
                     Shiboken::Conversions::copyToPython(converter, &index));

    auto *data = reinterpret_cast<QmlListPropertyPrivate *>(propList->data);
    Shiboken::AutoDecRef retVal(PyObject_CallObject(data->at, args));

    QObject *result = nullptr;
    if (PyErr_Occurred())
        PyErr_Print();
    else if (PyType_IsSubtype(Py_TYPE(retVal), data->type))
        Shiboken::Conversions::pythonToCppPointer(qobjectType, retVal, &result);
    return result;
}

// Implementation of QQmlListProperty<T>::ClearFunction callback
void propListClear(QQmlListProperty<QObject> * propList)
{
    Shiboken::GilState state;

    Shiboken::AutoDecRef args(PyTuple_New(1));
    PyTypeObject *qobjectType = PySide::qObjectType();
    PyTuple_SetItem(args, 0,
                     Shiboken::Conversions::pointerToPython(qobjectType, propList->object));

    auto *data = reinterpret_cast<QmlListPropertyPrivate *>(propList->data);
    Shiboken::AutoDecRef retVal(PyObject_CallObject(data->clear, args));

    if (PyErr_Occurred())
        PyErr_Print();
}

// Implementation of QQmlListProperty<T>::ReplaceFunction callback
void propListReplace(QQmlListProperty<QObject> *propList, qsizetype index, QObject *value)
{
    Shiboken::GilState state;

    Shiboken::AutoDecRef args(PyTuple_New(3));
    PyTypeObject *qobjectType = PySide::qObjectType();
    PyTuple_SetItem(args, 0,
                     Shiboken::Conversions::pointerToPython(qobjectType, propList->object));
    auto *converter = Shiboken::Conversions::PrimitiveTypeConverter<qsizetype>();
    PyTuple_SetItem(args, 1,
                     Shiboken::Conversions::copyToPython(converter, &index));
    PyTuple_SetItem(args, 2,
                     Shiboken::Conversions::pointerToPython(qobjectType, value));

    auto *data = reinterpret_cast<QmlListPropertyPrivate *>(propList->data);
    Shiboken::AutoDecRef retVal(PyObject_CallObject(data->replace, args));

    if (PyErr_Occurred())
        PyErr_Print();
}

// Implementation of QQmlListProperty<T>::RemoveLastFunction callback
void propListRemoveLast(QQmlListProperty<QObject> *propList)
{
    Shiboken::GilState state;

    Shiboken::AutoDecRef args(PyTuple_New(1));
    PyTypeObject *qobjectType = PySide::qObjectType();
    PyTuple_SetItem(args, 0,
                     Shiboken::Conversions::pointerToPython(qobjectType, propList->object));

    auto *data = reinterpret_cast<QmlListPropertyPrivate *>(propList->data);
    Shiboken::AutoDecRef retVal(PyObject_CallObject(data->removeLast, args));

    if (PyErr_Occurred())
        PyErr_Print();
}

// qt_metacall specialization for ListProperties
void QmlListPropertyPrivate::metaCall(PyObject *source, QMetaObject::Call call, void **args)
{
    if (call != QMetaObject::ReadProperty)
        return;

    QObject *qobj{};
    PyTypeObject *qobjectType = PySide::qObjectType();
    Shiboken::Conversions::pythonToCppPointer(qobjectType, source, &qobj);
    QQmlListProperty<QObject> declProp(
        qobj, this,
        append != nullptr ? &propListAppender : nullptr,
        count != nullptr ? &propListCount : nullptr,
        at != nullptr ? &propListAt : nullptr,
        clear != nullptr ? &propListClear : nullptr,
        replace != nullptr ? &propListReplace : nullptr,
        removeLast != nullptr ? &propListRemoveLast : nullptr);

    // Copy the data to the memory location requested by the meta call
    void *v = args[0];
    *reinterpret_cast<QQmlListProperty<QObject> *>(v) = declProp;
}

static const char *PropertyList_SignatureStrings[] = {
    "PySide6.QtQml.ListProperty(self,type:type,"
        "append:typing.Optional[collections.abc.Callable[...,typing.Any]]=None,"
        "at:typing.Optional[collections.abc.Callable[...,typing.Any]]=None,"
        "clear:typing.Optional[collections.abc.Callable[...,typing.Any]]=None,"
        "count:typing.Optional[collections.abc.Callable[...,typing.Any]]=None)",
    nullptr // Sentinel
};

namespace PySide::Qml {

void initQtQmlListProperty(PyObject *module)
{
    // Export QmlListProperty type
    if (InitSignatureStrings(PropertyList_TypeF(), PropertyList_SignatureStrings) < 0) {
        PyErr_Print();
        qWarning() << "Error initializing PropertyList type.";
        return;
    }

    // Register QQmlListProperty metatype for use in QML
    qRegisterMetaType<QQmlListProperty<QObject>>();

    auto *propertyListType = PropertyList_TypeF();
    auto *obPropertyListType = reinterpret_cast<PyObject *>(propertyListType);
    Py_INCREF(obPropertyListType);
    PepModule_AddType(module, propertyListType);
}

} // namespace PySide::Qml
