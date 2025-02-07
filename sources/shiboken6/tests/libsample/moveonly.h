// Copyright (C) 2025 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only WITH Qt-GPL-exception-1.0

#ifndef MOVEONLY_H
#define MOVEONLY_H

#include "libsamplemacros.h"

class MoveOnly
{
public:
    LIBMINIMAL_DISABLE_COPY(MoveOnly)
    LIBMINIMAL_DEFAULT_MOVE(MoveOnly)

    explicit MoveOnly(int v = 0) noexcept : m_value(v) {}
    ~MoveOnly() = default;

    int value() const { return m_value; }

private:
    int m_value;
};

class MoveOnlyHandler
{
public:
    LIBMINIMAL_DISABLE_COPY(MoveOnlyHandler)
    LIBMINIMAL_DISABLE_MOVE(MoveOnlyHandler)

    MoveOnlyHandler() noexcept = default;
    virtual ~MoveOnlyHandler() = default;

    static MoveOnly passMoveOnly(MoveOnly m) { return m; }

    // Test whether compilation succeeds
    virtual MoveOnly passMoveOnlyVirtually(MoveOnly m) { return m; }
};

#endif // MOVEONLY_H
