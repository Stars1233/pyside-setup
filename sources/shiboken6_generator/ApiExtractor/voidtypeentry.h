// Copyright (C) 2022 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only WITH Qt-GPL-exception-1.0

#ifndef VOIDTYPEENTRY_H
#define VOIDTYPEENTRY_H

#include "cpptypeentry.h"

class VoidTypeEntry : public CppTypeEntry
{
public:
    VoidTypeEntry();

    TypeEntry *clone() const override;

protected:
    explicit VoidTypeEntry(CppTypeEntryPrivate *d);
};

#endif // VOIDTYPEENTRY_H
