# Copyright (C) 2022 The Qt Company Ltd.
# Copyright (C) 2011 Thomas Perl <thp.io/about>
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only WITH Qt-GPL-exception-1.0
from __future__ import annotations

# Test case for PySide bug 829

import gc
import os
import subprocess
import sys
import unittest

from pathlib import Path
sys.path.append(os.fspath(Path(__file__).resolve().parents[1]))
from init_paths import init_test_paths
init_test_paths(False)

from PySide6.QtCore import QDir, QSettings, QTemporaryFile


class QVariantConversions(unittest.TestCase):

    _confFileName = None

    def testDictionary(self):
        '''Builtin dict round-trips through QSettings without any opt-in'''
        confFile = QTemporaryFile(QDir.tempPath() + '/pysidebug829_XXXXXX.ini')
        confFile.setAutoRemove(False)
        self.assertTrue(confFile.open())
        confFile.close()
        self._confFileName = confFile.fileName()
        del confFile
        # PYSIDE-535: Need to collect garbage in PyPy to trigger deletion
        gc.collect()
        s = QSettings(self._confFileName, QSettings.Format.IniFormat)
        self.assertEqual(s.status(), QSettings.Status.NoError)
        s.setValue('x', {1: 'a'})
        s.sync()
        self.assertEqual(s.status(), QSettings.Status.NoError)
        del s
        gc.collect()

        s = QSettings(self._confFileName, QSettings.Format.IniFormat)
        self.assertEqual(s.status(), QSettings.Status.NoError)
        self.assertEqual(s.value('x'), {1: 'a'})

    def testCustomClassRejected(self):
        '''Custom (non-builtin) Python classes stored in QSettings raise RuntimeError on read.

        The write is performed in a subprocess so Qt's in-process QConfFile cache
        does not short-circuit the disk read in the reader process.  This reflects
        the real attack: a settings file written with an arbitrary class is read by
        another process that only allows builtin types.
        '''
        confFile = QTemporaryFile(QDir.tempPath() + '/pysidebug829_r16_XXXXXX.ini')
        confFile.setAutoRemove(False)
        self.assertTrue(confFile.open())
        confFile.close()
        fname = confFile.fileName()
        del confFile
        gc.collect()

        # Write a custom-class instance from a subprocess.
        # operator<< (serialize) is unrestricted; operator>> (deserialize) is restricted.
        write_script = (
            "import sys;"
            f"sys.path.append({str(Path(__file__).resolve().parents[1])!r});"
            "from init_paths import init_test_paths; init_test_paths(False);"
            "from PySide6.QtCore import QSettings;"
            "_Foo = type('_Foo', (), {});"
            f"s = QSettings({QDir.toNativeSeparators(fname)!r}, QSettings.Format.IniFormat);"
            "s.setValue('x', _Foo()); s.sync()"
        )
        subprocess.run([sys.executable, '-c', write_script], check=True)

        # Reading a non-builtin type must raise RuntimeError
        s = QSettings(fname, QSettings.Format.IniFormat)
        with self.assertRaises(RuntimeError):
            s.value('x')
        del s
        try:
            os.unlink(QDir.toNativeSeparators(fname))
        except OSError:
            pass

    def __del__(self):
        if self._confFileName is not None:
            os.unlink(QDir.toNativeSeparators(self._confFileName))


if __name__ == '__main__':
    unittest.main()
