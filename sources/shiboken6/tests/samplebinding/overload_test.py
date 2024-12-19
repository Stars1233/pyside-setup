#!/usr/bin/env python
# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only WITH Qt-GPL-exception-1.0
from __future__ import annotations

'''Test cases for Overload class'''

import os
import sys
import unittest

from pathlib import Path
sys.path.append(os.fspath(Path(__file__).resolve().parents[1]))
from shiboken_paths import init_paths
init_paths()
from sample import Echo, Overload, Point, PointF, Polygon, Rect, RectF, Size, Str


def raisesWithErrorMessage(func, arguments, errorType, errorMsg):
    '''NOTE: Using 'try' because assertRaisesRegexp is not available
       to check the error message.'''
    try:
        func(*arguments)
        return False
    except TypeError as err:
        return errorMsg in str(err)
    except Exception:
        return False
    return True


class OverloadTest(unittest.TestCase):
    '''Test case for Overload class'''

    def testOverloadMethod0(self):
        '''Check overloaded method call for signature "overloaded()".'''
        overload = Overload()
        self.assertEqual(overload.overloaded(), Overload.FunctionEnum.Function0)

    def testOverloadMethod1(self):
        '''Check overloaded method call for signature "overloaded(Size*)".'''
        overload = Overload()
        size = Size()
        self.assertEqual(overload.overloaded(size), Overload.FunctionEnum.Function1)

    def testOverloadMethod2(self):
        '''Check overloaded method call for signature "overloaded(Point*, ParamEnum)".'''
        overload = Overload()
        point = Point()
        self.assertEqual(overload.overloaded(point, Overload.ParamEnum.Param1),
                         Overload.FunctionEnum.Function2)

    def testOverloadMethod3(self):
        '''Check overloaded method call for signature "overloaded(const Point&)".'''
        overload = Overload()
        point = Point()
        self.assertEqual(overload.overloaded(point), Overload.FunctionEnum.Function3)

    def testDifferentReturnTypes(self):
        '''Check method calls for overloads with different return types.'''
        overload = Overload()
        self.assertEqual(overload.differentReturnTypes(), None)
        self.assertEqual(overload.differentReturnTypes(Overload.ParamEnum.Param1), None)
        self.assertEqual(overload.differentReturnTypes(Overload.ParamEnum.Param0, 13), 13)

    def testIntOverloads(self):
        overload = Overload()
        self.assertEqual(overload.intOverloads(2, 3), 2)
        self.assertEqual(overload.intOverloads(2, 4.5), 3)
        self.assertEqual(overload.intOverloads(Point(0, 0), 3), 1)

    def testIntDoubleOverloads(self):
        overload = Overload()
        self.assertEqual(overload.intDoubleOverloads(1, 2), Overload.FunctionEnum.Function0)
        self.assertEqual(overload.intDoubleOverloads(1, 2.0), Overload.FunctionEnum.Function0)
        self.assertEqual(overload.intDoubleOverloads(1.0, 2), Overload.FunctionEnum.Function1)
        self.assertEqual(overload.intDoubleOverloads(1.0, 2.0), Overload.FunctionEnum.Function1)

    def testWrapperIntIntOverloads(self):
        overload = Overload()
        self.assertEqual(overload.wrapperIntIntOverloads(Point(), 1, 2),
                         Overload.FunctionEnum.Function0)
        self.assertEqual(overload.wrapperIntIntOverloads(Polygon(), 1, 2),
                         Overload.FunctionEnum.Function1)

    def testDrawTextPointAndStr(self):
        overload = Overload()
        self.assertEqual(overload.drawText(Point(), Str()), Overload.FunctionEnum.Function0)
        self.assertEqual(overload.drawText(Point(), ''), Overload.FunctionEnum.Function0)
        self.assertEqual(overload.drawText(PointF(), Str()), Overload.FunctionEnum.Function1)
        self.assertEqual(overload.drawText(PointF(), ''), Overload.FunctionEnum.Function1)

    def testDrawTextRectIntStr(self):
        overload = Overload()
        self.assertEqual(overload.drawText(Rect(), 1, Str()), Overload.FunctionEnum.Function2)
        self.assertEqual(overload.drawText(Rect(), 1, ''), Overload.FunctionEnum.Function2)
        self.assertEqual(overload.drawText(RectF(), 1, Str()), Overload.FunctionEnum.Function3)
        self.assertEqual(overload.drawText(RectF(), 1, ''), Overload.FunctionEnum.Function3)

    def testDrawTextRectFStrEcho(self):
        overload = Overload()
        self.assertEqual(overload.drawText(RectF(), Str()), Overload.FunctionEnum.Function4)
        self.assertEqual(overload.drawText(RectF(), ''), Overload.FunctionEnum.Function4)
        self.assertEqual(overload.drawText(RectF(), Str(), Echo()), Overload.FunctionEnum.Function4)
        self.assertEqual(overload.drawText(RectF(), '', Echo()), Overload.FunctionEnum.Function4)
        self.assertEqual(overload.drawText(Rect(), Str()), Overload.FunctionEnum.Function4)
        self.assertEqual(overload.drawText(Rect(), ''), Overload.FunctionEnum.Function4)
        self.assertEqual(overload.drawText(Rect(), Str(), Echo()), Overload.FunctionEnum.Function4)
        self.assertEqual(overload.drawText(Rect(), '', Echo()), Overload.FunctionEnum.Function4)

    def testDrawTextIntIntStr(self):
        overload = Overload()
        self.assertEqual(overload.drawText(1, 2, Str()), Overload.FunctionEnum.Function5)
        self.assertEqual(overload.drawText(1, 2, ''), Overload.FunctionEnum.Function5)

    def testDrawTextIntIntIntIntStr(self):
        overload = Overload()
        self.assertEqual(overload.drawText(1, 2, 3, 4, 5, Str()), Overload.FunctionEnum.Function6)
        self.assertEqual(overload.drawText(1, 2, 3, 4, 5, ''), Overload.FunctionEnum.Function6)

    def testDrawText2IntIntIntIntStr(self):
        overload = Overload()
        self.assertEqual(overload.drawText2(1, 2, 3, 4, 5, Str()), Overload.FunctionEnum.Function6)
        self.assertEqual(overload.drawText2(1, 2, 3, 4, 5, ''), Overload.FunctionEnum.Function6)
        self.assertEqual(overload.drawText2(1, 2, 3, 4, 5), Overload.FunctionEnum.Function6)
        self.assertEqual(overload.drawText2(1, 2, 3, 4), Overload.FunctionEnum.Function6)
        self.assertEqual(overload.drawText2(1, 2, 3), Overload.FunctionEnum.Function6)

    def testDrawText3(self):
        overload = Overload()
        self.assertEqual(overload.drawText3(Str(), Str(), Str()), Overload.FunctionEnum.Function0)
        self.assertEqual(overload.drawText3('', '', ''), Overload.FunctionEnum.Function0)
        self.assertEqual(overload.drawText3(1, 2, 3, 4, 5), Overload.FunctionEnum.Function1)
        self.assertEqual(overload.drawText3(1, 2, 3, 4, 5), Overload.FunctionEnum.Function1)

    def testDrawText3Exception(self):
        overload = Overload()
        args = (Str(), Str(), Str(), 4, 5)
        result = raisesWithErrorMessage(overload.drawText3, args,
                                        TypeError, 'called with wrong argument types:')
        self.assertTrue(result)

    def testDrawText4(self):
        overload = Overload()
        self.assertEqual(overload.drawText4(1, 2, 3), Overload.FunctionEnum.Function0)
        self.assertEqual(overload.drawText4(1, 2, 3, 4, 5), Overload.FunctionEnum.Function1)

    def testAcceptSequence(self):
        # Overload.acceptSequence()
        overload = Overload()
        self.assertEqual(overload.acceptSequence(), Overload.FunctionEnum.Function0)

    def testAcceptSequenceIntInt(self):
        # Overload.acceptSequence(int,int)
        overload = Overload()
        self.assertEqual(overload.acceptSequence(1, 2), Overload.FunctionEnum.Function1)

    def testAcceptSequenceStrParamEnum(self):
        # Overload.acceptSequence(Str,Overload::ParamEnum)
        overload = Overload()
        self.assertEqual(overload.acceptSequence(''), Overload.FunctionEnum.Function2)
        self.assertEqual(overload.acceptSequence('', Overload.ParamEnum.Param0),
                         Overload.FunctionEnum.Function2)
        self.assertEqual(overload.acceptSequence(Str('')), Overload.FunctionEnum.Function2)
        self.assertEqual(overload.acceptSequence(Str(''), Overload.ParamEnum.Param0),
                         Overload.FunctionEnum.Function2)

    def testAcceptSequenceSize(self):
        # Overload.acceptSequence(Size)
        overload = Overload()
        self.assertEqual(overload.acceptSequence(Size()), Overload.FunctionEnum.Function3)

    def testAcceptSequenceStringList(self):
        # Overload.acceptSequence(const char**)
        overload = Overload()
        strings = ['line 1', 'line 2']
        self.assertEqual(overload.acceptSequence(strings), Overload.FunctionEnum.Function4)
        args = (['line 1', 2], )
        result = raisesWithErrorMessage(overload.acceptSequence, args,
                                        TypeError, 'The argument must be a sequence of strings.')
        self.assertTrue(result)

    def testAcceptSequencePyObject(self):
        # Overload.acceptSequence(void*)
        overload = Overload()

        class Foo:
            pass

        foo = Foo()
        self.assertEqual(overload.acceptSequence(foo), Overload.FunctionEnum.Function5)


if __name__ == '__main__':
    unittest.main()
