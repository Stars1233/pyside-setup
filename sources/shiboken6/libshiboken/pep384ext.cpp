// Copyright (C) 2026 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only

#include "pep384ext.h"
#include "autodecref.h"
#include "sbkstaticstrings_p.h"
#include "sbkstring.h"

const char *PepExt_TypeGetQualName(PyTypeObject *type)
{
    Shiboken::AutoDecRef qualName(PepType_GetQualName(type));
    return qualName.isNull() ? type->tp_name : Shiboken::String::toCString(qualName.object());
}

static PyObject *runPyScriptHelper(const char *moduleName, const char *script, int start)
{
    PyObject *module = PyImport_AddModule(moduleName);
    if (module == nullptr)
        return nullptr;
    PyObject *globalDictionary = PyModule_GetDict(module);
    Shiboken::AutoDecRef localDictionary(PyDict_New());
    // Note: Limited API only has PyRun_String()
    return PyRun_String(script, start, globalDictionary, localDictionary.object());
}

PyObject *PepExt_RunString(const char *script)
{
    return runPyScriptHelper("__main__", script, Py_file_input);
}

PyObject *PepExt_EvalString(const char *script)
{
    return runPyScriptHelper("__main__", script, Py_eval_input);
}

PyObject *PepExt_EvalString(const char *module, const char *script)
{
    return runPyScriptHelper(module, script, Py_eval_input);
}
