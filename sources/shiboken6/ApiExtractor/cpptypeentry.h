// Copyright (C) 2025 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only WITH Qt-GPL-exception-1.0

#ifndef CPPTYPEENTRY_H
#define CPPTYPEENTRY_H

#include "typesystem.h"
#include "typesystem_enums.h"

class CppTypeEntryPrivate;

class CppTypeEntry : public TypeEntry
{
public:
    explicit CppTypeEntry(const QString &entryName, Type t, const QVersionNumber &vr,
                          const TypeEntryCPtr &parent);

    const QString &defaultConstructor() const;
    void setDefaultConstructor(const QString& defaultConstructor);
    bool hasDefaultConstructor() const { return !defaultConstructor().isEmpty(); }

    // View on: Type to use for function argument conversion, fex
    // "std::string_view" -> "std::string" for "foo(std::string_view)".
    // cf AbstractMetaType::viewOn()
    CppTypeEntryCPtr viewOn() const;
    void setViewOn(const CppTypeEntryCPtr &v);

    TypeEntry *clone() const override;

#ifndef QT_NO_DEBUG_STREAM
    void formatDebug(QDebug &debug) const override;
#endif

protected:
    explicit CppTypeEntry(CppTypeEntryPrivate *d);
};

#endif // CPPTYPEENTRY_H
