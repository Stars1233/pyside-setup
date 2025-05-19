// Copyright (C) 2016 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only WITH Qt-GPL-exception-1.0

#include "bucket.h"

#include <iostream>

#ifdef _WIN32 // _WIN32 is defined by all Windows 32 and 64 bit compilers, but not by others.
#  ifndef WIN32_LEAN_AND_MEAN
#    define WIN32_LEAN_AND_MEAN
#  endif
#  include <windows.h>
#  define SLEEP(x) Sleep(x)
#else
#  include <unistd.h>
#  define SLEEP(x) usleep(x)
#endif

void Bucket::push(int x)
{
    m_data.push_back(x);
}

int Bucket::pop(void)
{
    int x = 0;

    if (!m_data.empty()) {
        x = m_data.front();
        m_data.pop_front();
    }

    return x;
}

bool Bucket::empty()
{
    return m_data.empty();
}

void Bucket::lock()
{
    bool expected = false;
    if (m_locked.compare_exchange_strong(expected, true)) {
        while (m_locked) {
            SLEEP(300);
        }
    } else {
        std::cerr << __FUNCTION__ << " Attempt to lock twice.\n";
    }
}

void Bucket::unlock()
{
    bool expected = true;
    if (!m_locked.compare_exchange_strong(expected, false))
        std::cerr << __FUNCTION__ << " Attempt to unlock twice.\n";
}

bool Bucket::virtualBlockerMethod()
{
    lock();
    // The return value was added just for diversity sake.
    return true;
}
