// Copyright (C) 2021 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only WITH Qt-GPL-exception-1.0

#include "derivedusingct.h"

void DerivedUsingCt::foo()
{
    delete new DerivedUsingCt(42);
}

int DerivedUsingCt::derivedValue() const
{
    return m_derivedValue;
}
