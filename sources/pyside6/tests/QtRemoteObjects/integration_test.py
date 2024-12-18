#!/usr/bin/python
# Copyright (C) 2025 Ford Motor Company
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only WITH Qt-GPL-exception-1.0
from __future__ import annotations

'''Test cases for basic Source/Replica communication'''

import os
import sys
import textwrap
import enum
import gc

import unittest

from pathlib import Path
sys.path.append(os.fspath(Path(__file__).resolve().parents[1]))
from init_paths import init_test_paths
init_test_paths(False)

from PySide6.QtCore import QUrl, qWarning
from PySide6.QtRemoteObjects import (QRemoteObjectHost, QRemoteObjectNode, QRemoteObjectReplica,
                                     QRemoteObjectPendingCall, RepFile, getCapsuleCount)
from PySide6.QtTest import QSignalSpy, QTest

from test_shared import wrap_tests_for_cleanup
from helper.usesqapplication import UsesQApplication

contents = """
class Simple
{
    PROP(int i = 2);
    PROP(float f = -1. READWRITE);
    SIGNAL(random(int i));
    SLOT(void reset());
    SLOT(int add(int i));
};
"""


class QBasicTest(UsesQApplication):
    '''Test case for basic source/replica communication'''
    def setUp(self):
        # Separate output to make debugging easier
        qWarning(f"\nSet up {self.__class__.__qualname__}")
        super().setUp()
        '''Set up test environment'''
        if hasattr(self.__class__, "contents"):
            qWarning(f"Using class contents >{self.__class__.contents}<")
            self.rep = RepFile(self.__class__.contents)
        else:
            self.rep = RepFile(contents)
        self.host = QRemoteObjectHost(QUrl("tcp://127.0.0.1:0"))
        self.host.setObjectName("host")
        self.node = QRemoteObjectNode()
        self.node.setObjectName("node")
        self.node.connectToNode(self.host.hostUrl())     # pick up the url with the assigned port

    def compare_properties(self, instance, values):
        '''Compare properties of instance with values'''
        self.assertEqual(instance.i, values[0])
        self.assertAlmostEqual(instance.f, values[1], places=5)

    def default_setup(self):
        '''Set up default test environment'''
        replica = self.node.acquire(self.rep.replica["Simple"])
        # Make sure the replica is initialized with default values
        self.compare_properties(replica, [2, -1])
        self.assertEqual(replica.isInitialized(), False)
        source = self.rep.source["Simple"]()
        # Make sure the source is initialized with default values
        self.compare_properties(source, [2, -1])
        return replica, source

    def tearDown(self):
        self.assertEqual(getCapsuleCount(), 0)
        self.app.processEvents()
        super().tearDown()
        # Separate output to make debugging easier
        qWarning(f"Tore down {self.__class__.__qualname__}\n")


@wrap_tests_for_cleanup(extra=['rep', 'host', 'node'])
class ReplicaInitialization(QBasicTest):
    def test_ReplicaInitialization(self):
        replica, source = self.default_setup()
        source.i = -1
        source.f = 3.14
        self.compare_properties(source, [-1, 3.14])
        init_spy = QSignalSpy(replica.initialized)
        self.host.enableRemoting(source)
        self.assertEqual(replica.waitForSource(1000), True)
        self.assertEqual(replica.state(), QRemoteObjectReplica.State.Valid)
        # Make sure the replica values are updated to the source values
        self.compare_properties(replica, [-1, 3.14])
        self.assertEqual(init_spy.count(), 1)
        self.assertEqual(replica.isInitialized(), True)


@wrap_tests_for_cleanup(extra=['rep', 'host', 'node'])
class SourcePropertyChange(QBasicTest):
    def test_SourcePropertyChange(self):
        replica, source = self.default_setup()
        self.host.enableRemoting(source)
        self.assertEqual(replica.waitForSource(1000), True)
        # Make sure the replica values are unchanged since the source had the same values
        self.compare_properties(replica, [2, -1])
        source_spy = QSignalSpy(source.iChanged)
        replica_spy = QSignalSpy(replica.iChanged)
        source.i = 42
        self.assertEqual(source_spy.count(), 1)
        # Make sure the source value is updated
        self.compare_properties(source, [42, source.f])
        self.assertTrue(replica_spy.wait(1000))
        self.assertEqual(replica_spy.count(), 1)
        # Make sure the replica value is updated
        self.compare_properties(replica, [42, replica.f])


@wrap_tests_for_cleanup(extra=['rep', 'host', 'node'])
class ReplicaPropertyChange(QBasicTest):
    def test_ReplicaPropertyChange(self):
        replica, source = self.default_setup()
        self.host.enableRemoting(source)
        self.assertEqual(replica.waitForSource(1000), True)
        # Make sure push methods are working
        source_spy = QSignalSpy(source.iChanged)
        replica_spy = QSignalSpy(replica.iChanged)
        replica.pushI(11)
        # # Let eventloop run to update the source and verify the values
        self.assertTrue(source_spy.wait(1000))
        self.assertEqual(source_spy.count(), 1)
        self.compare_properties(source, [11, source.f])
        # Let eventloop run to update the replica and verify the values
        self.assertTrue(replica_spy.wait(1000))
        self.assertEqual(replica_spy.count(), 1)
        self.compare_properties(replica, [11, replica.f])

        # Test setter on replica
        source_spy = QSignalSpy(source.fChanged)
        replica_spy = QSignalSpy(replica.fChanged)
        replica.f = 4.2
        # Make sure the replica values are ** NOT CHANGED ** since the eventloop hasn't run
        self.compare_properties(replica, [11, -1])
        # Let eventloop run to update the source and verify the values
        self.assertTrue(source_spy.wait(1000))
        self.assertEqual(source_spy.count(), 1)
        self.compare_properties(source, [source.i, 4.2])
        # Let eventloop run to update the replica and verify the values
        self.assertTrue(replica_spy.wait(1000))
        self.assertEqual(replica_spy.count(), 1)
        self.compare_properties(replica, [replica.i, 4.2])


@wrap_tests_for_cleanup(extra=['rep', 'host', 'node'])
class DerivedReplicaPropertyChange(QBasicTest):
    def test_DerivedReplicaPropertyChange(self):
        # Don't use default_setup(), instead create a derived replica
        Replica = self.rep.replica["Simple"]

        class DerivedReplica(Replica):
            pass

        replica = self.node.acquire(DerivedReplica)
        # Make sure the replica is initialized with default values
        self.compare_properties(replica, [2, -1])
        self.assertEqual(replica.isInitialized(), False)
        source = self.rep.source["Simple"]()
        self.host.enableRemoting(source)
        self.assertEqual(replica.waitForSource(1000), True)


@wrap_tests_for_cleanup(extra=['rep', 'host', 'node'])
class ReplicaSlotNotImplementedChange(QBasicTest):
    def test_ReplicaSlotNotImplementedChange(self):
        replica, source = self.default_setup()
        self.host.enableRemoting(source)
        self.assertEqual(replica.waitForSource(1000), True)
        # Ideally this would fail as the slot is not implemented on the source
        res = replica.reset()
        self.assertEqual(type(res), type(None))
        QTest.qWait(100)  # Wait for 100 ms for async i/o.  There isn't a signal to wait on
        res = replica.add(5)
        self.assertEqual(type(res), QRemoteObjectPendingCall)


@wrap_tests_for_cleanup(extra=['rep', 'host', 'node'])
class ReplicaSlotImplementedChange(QBasicTest):
    def test_ReplicaSlotImplementedChange(self):
        replica = self.node.acquire(self.rep.replica["Simple"])
        replica.setObjectName("replica")

        class Source(self.rep.source["Simple"]):
            def __init__(self):
                super().__init__()
                self.i = 6
                self.f = 3.14

            def reset(self):
                self.i = 0
                self.f = 0

            def add(self, i):
                return self.i + i

        source = Source()
        source.setObjectName("source")
        self.host.enableRemoting(source)
        self.assertEqual(replica.waitForSource(1000), True)
        self.compare_properties(source, [6, 3.14])
        self.compare_properties(replica, [6, 3.14])
        replica_spy = QSignalSpy(replica.iChanged)
        res = replica.reset()
        self.assertEqual(type(res), type(None))
        self.assertEqual(replica_spy.wait(1000), True)
        self.compare_properties(source, [0, 0])
        self.compare_properties(replica, [0, 0])
        res = replica.add(5)
        self.assertEqual(type(res), QRemoteObjectPendingCall)
        self.assertEqual(res.waitForFinished(1000), True)
        self.assertEqual(res.returnValue(), 5)


@wrap_tests_for_cleanup(extra=['rep', 'host', 'node'])
class RefCountTest(QBasicTest):
    contents = textwrap.dedent("""\
        POD MyPOD{
            ENUM class Position : unsigned short {position1=1, position2=2, position3=4}
            Position pos,
            QString name
        }
        class Simple
        {
            ENUM Position {Left, Right, Top, Bottom}
            PROP(MyPOD myPod);
            PROP(Position pos);
        }
        """)

    def test_RefCount(self):
        # Once the rep file is loaded, we should be tracking 4 converter capsules
        # - 1 for the POD itself
        # - 1 for the enum in the POD
        # - 1 for the enum in the Source
        # - 1 for the enum in the Replica
        # We should be tracking 3 qobject capsules (POD, Replica, Source)
        # Note: Source and Replica are distinct types, so Source::EPosition and
        # Replica::EPosition are distinct as well.
        # Note 2: The name of the enum ("Position") can be reused for different
        # types in different classes as shown above.
        self.assertEqual(getCapsuleCount(), 7)
        MyPod = self.rep.pod["MyPOD"]
        self.assertTrue(isinstance(MyPod, type))
        self.assertTrue(issubclass(MyPod, tuple))
        MyEnum = MyPod.get_enum("Position")
        self.assertTrue(isinstance(MyEnum, type))
        self.assertTrue(issubclass(MyEnum, enum.Enum))
        e = MyEnum(4)  # noqa: F841
        Source = self.rep.source["Simple"]
        source = Source()  # noqa: F841
        source = None  # noqa: F841
        Source = None
        Replica = self.rep.replica["Simple"]
        replica = self.node.acquire(Replica)  # noqa: F841
        replica = None  # noqa: F841
        Replica = None
        MyEnum = None
        MyPod = None
        self.rep = None
        e = None  # noqa: F841
        gc.collect()
        # The enum and POD capsules will only be deleted (garbage collected) if
        # the types storing them (RepFile, Replica and Source) are garbage
        # collected first.
        self.assertEqual(getCapsuleCount(), 0)


@wrap_tests_for_cleanup(extra=['rep', 'host', 'node'])
class EnumTest(QBasicTest):
    contents = textwrap.dedent("""\
        POD MyPOD{
            ENUM class Position : unsigned short {position1=1, position2=2, position3=4}
            Position pos,
            QString name
        }
        class Simple
        {
            ENUM Position {Left, Right, Top, Bottom}
            PROP(MyPOD myPod);
            PROP(Position pos);
        }
        """)

    def test_Enum(self):
        MyPod = self.rep.pod["MyPOD"]
        self.assertTrue(isinstance(MyPod, type))
        self.assertTrue(issubclass(MyPod, tuple))
        PodEnum = MyPod.get_enum("Position")
        self.assertTrue(isinstance(PodEnum, type))
        self.assertTrue(issubclass(PodEnum, enum.Enum))
        t = (PodEnum(4), "test")
        myPod = MyPod(*t)
        with self.assertRaises(ValueError):
            myPod = MyPod(PodEnum(0), "thing")  # 0 isn't a valid enum value
        myPod = MyPod(PodEnum(2), "thing")
        self.assertEqual(myPod.pos, PodEnum.position2)
        replica = self.node.acquire(self.rep.replica["Simple"])
        replica.setObjectName("replica")
        source = self.rep.source["Simple"]()
        source.setObjectName("source")
        source.myPod = (PodEnum.position2, "Hello")
        SourceEnum = source.get_enum("Position")
        self.assertTrue(isinstance(SourceEnum, type))
        self.assertTrue(issubclass(SourceEnum, enum.Enum))
        source.pos = SourceEnum.Top
        self.assertEqual(source.myPod, (PodEnum.position2, "Hello"))
        self.assertNotEqual(source.pos, 2)
        self.host.enableRemoting(source)
        self.assertEqual(replica.waitForSource(1000), True)
        self.assertEqual(replica.myPod, (PodEnum.position2, "Hello"))
        ReplicaEnum = replica.get_enum("Position")
        # Test invalid comparisons
        self.assertNotEqual(replica.pos, 2)
        self.assertNotEqual(replica.pos, SourceEnum.Top)
        self.assertNotEqual(replica.myPod, (SourceEnum(2), "Hello"))
        self.assertNotEqual(replica.myPod, (ReplicaEnum(2), "Hello"))
        self.assertNotEqual(replica.myPod, (2, "Hello"))
        # Test valid comparisons to Replica enum
        self.assertEqual(replica.pos, ReplicaEnum.Top)
        self.assertEqual(replica.myPod, (PodEnum(2), "Hello"))


@wrap_tests_for_cleanup(extra=['rep', 'host', 'node'])
class PodTest(QBasicTest):
    contents = textwrap.dedent("""\
        POD MyPod(int i, QString s)

        class Simple
        {
            PROP(MyPod pod);
        }
        """)

    def test_Pod(self):
        MyPod = self.rep.pod["MyPod"]
        self.assertTrue(isinstance(MyPod, type))
        self.assertTrue(issubclass(MyPod, tuple))
        source = self.rep.source["Simple"]()
        t = (42, "Hello")
        pod = MyPod(*t)
        source.pod = t
        self.assertEqual(source.pod, t)
        self.assertEqual(source.pod, pod)
        source.pod = pod
        self.assertEqual(source.pod, t)
        self.assertEqual(source.pod, pod)
        with self.assertRaises(ValueError):
            source.pod = (11, "World", "!")
        with self.assertRaises(TypeError):
            source.pod = MyPod("Hello", "World")
        self.assertEqual(source.pod, pod)
        self.assertTrue(isinstance(pod, MyPod))
        self.assertEqual(pod.i, 42)
        self.assertEqual(pod.s, "Hello")
        self.assertTrue(isinstance(source.pod, MyPod))


if __name__ == '__main__':
    unittest.main()
