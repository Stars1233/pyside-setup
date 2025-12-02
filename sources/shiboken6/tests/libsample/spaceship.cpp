// Copyright (C) 2025 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only WITH Qt-GPL-exception-1.0

#include "spaceship.h"

SpaceshipComparisonTester::SpaceshipComparisonTester(int v) noexcept
    : m_value(v)
{
}

FreeSpaceshipComparisonTester::FreeSpaceshipComparisonTester(int v) noexcept
    : m_value(v)
{
}

int FreeSpaceshipComparisonTester::value() const
{
    return m_value;
}

#if __cplusplus >= 202002 || (defined(_MSVC_LANG) && _MSVC_LANG >= 202002)
std::strong_ordering operator<=>(FreeSpaceshipComparisonTester lhs,
                                 FreeSpaceshipComparisonTester rhs)
{
    return lhs.value() <=> rhs.value();
}
#endif // C++ 20
