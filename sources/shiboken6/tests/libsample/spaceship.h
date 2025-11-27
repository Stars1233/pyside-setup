// Copyright (C) 2025 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only WITH Qt-GPL-exception-1.0

#ifndef SPACESHIP_H
#define SPACESHIP_H

#include "libsamplemacros.h"

#if __cplusplus >= 202002 || (defined(_MSVC_LANG) && _MSVC_LANG >= 202002)
#  include <compare>
#endif

class LIBSAMPLE_API SpaceshipComparisonTester
{
public:
    explicit SpaceshipComparisonTester(int v) noexcept;

#if __cplusplus >= 202002 || (defined(_MSVC_LANG) && _MSVC_LANG >= 202002)
    auto operator<=>(const SpaceshipComparisonTester &rhs) const = default;
    std::strong_ordering operator<=>(int rhs) const;

    enum Enabled { HasSpaceshipOperator = 1 };
#else
    enum Enabled { HasSpaceshipOperator = 0 };
#endif // C++ 20

private:
    int m_value;
};

class LIBSAMPLE_API FreeSpaceshipComparisonTester
{
public:
    explicit FreeSpaceshipComparisonTester(int v) noexcept;

    int value() const;

private:
    int m_value;
};

#if __cplusplus >= 202002 || (defined(_MSVC_LANG) && _MSVC_LANG >= 202002)
// Does not provide equality as it is not defaulted.
LIBSAMPLE_API std::strong_ordering operator<=>(FreeSpaceshipComparisonTester lhs,
                                               FreeSpaceshipComparisonTester rhs);
#endif // C++ 20

#endif // SPACESHIP_H
