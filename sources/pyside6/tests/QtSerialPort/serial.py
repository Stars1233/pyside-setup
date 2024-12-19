#!/usr/bin/python
# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only WITH Qt-GPL-exception-1.0
from __future__ import annotations

'''Test cases for QSerialPort'''

import os
import sys
import unittest

from pathlib import Path
sys.path.append(os.fspath(Path(__file__).resolve().parents[1]))
from init_paths import init_test_paths  # noqa: E402
init_test_paths(False)

from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo  # noqa: E402
from PySide6.QtCore import QIODevice  # noqa: E402


class QSerialPortTest(unittest.TestCase):
    def testDefaultConstructedPort(self):
        serialPort = QSerialPort()

        self.assertEqual(serialPort.error(), QSerialPort.SerialPortError.NoError)
        self.assertTrue(not serialPort.errorString() == "")

        # properties
        defaultBaudRate = QSerialPort.BaudRate.Baud9600
        self.assertEqual(serialPort.baudRate(), defaultBaudRate)
        self.assertEqual(serialPort.baudRate(QSerialPort.Direction.Input), defaultBaudRate)
        self.assertEqual(serialPort.baudRate(QSerialPort.Direction.Output), defaultBaudRate)
        self.assertEqual(serialPort.dataBits(), QSerialPort.DataBits.Data8)
        self.assertEqual(serialPort.parity(), QSerialPort.Parity.NoParity)
        self.assertEqual(serialPort.stopBits(), QSerialPort.StopBits.OneStop)
        self.assertEqual(serialPort.flowControl(), QSerialPort.FlowControl.NoFlowControl)

        self.assertEqual(serialPort.pinoutSignals(), QSerialPort.PinoutSignal.NoSignal)
        self.assertEqual(serialPort.isRequestToSend(), False)
        self.assertEqual(serialPort.isDataTerminalReady(), False)

        # QIODevice
        self.assertEqual(serialPort.openMode(), QIODevice.OpenModeFlag.NotOpen)
        self.assertTrue(not serialPort.isOpen())
        self.assertTrue(not serialPort.isReadable())
        self.assertTrue(not serialPort.isWritable())
        self.assertTrue(serialPort.isSequential())
        self.assertEqual(serialPort.canReadLine(), False)
        self.assertEqual(serialPort.pos(), 0)
        self.assertEqual(serialPort.size(), 0)
        self.assertTrue(serialPort.atEnd())
        self.assertEqual(serialPort.bytesAvailable(), 0)
        self.assertEqual(serialPort.bytesToWrite(), 0)

    def testOpenExisting(self):
        allportinfos = QSerialPortInfo.availablePorts()
        for portinfo in allportinfos:
            serialPort = QSerialPort(portinfo)
            self.assertEqual(serialPort.portName(), portinfo.portName())


class QSerialPortInfoTest(unittest.TestCase):
    def test_available_ports(self):
        allportinfos = QSerialPortInfo.availablePorts()
        for portinfo in allportinfos:
            portinfo.description()
            portinfo.hasProductIdentifier()
            portinfo.hasVendorIdentifier()
            portinfo.isNull()


if __name__ == '__main__':
    unittest.main()
