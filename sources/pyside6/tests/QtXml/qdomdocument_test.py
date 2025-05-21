#!/usr/bin/python
# Copyright (C) 2022 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only WITH Qt-GPL-exception-1.0
from __future__ import annotations

import gc
import os
import sys
import unittest

from pathlib import Path
sys.path.append(os.fspath(Path(__file__).resolve().parents[1]))
from init_paths import init_test_paths
init_test_paths(False)

from PySide6.QtCore import QByteArray
from PySide6.QtXml import QDomDocument, QDomElement


class QDomDocumentTest(unittest.TestCase):

    def setUp(self):
        self.dom = QDomDocument()

        self.goodXmlData = QByteArray(bytes('''
        <typesystem package="PySide6.QtXml">
            <value-type name="QDomDocument"/>
            <value-type name="QDomElement"/>
        </typesystem>
        ''', "UTF-8"))

        self.badXmlData = QByteArray(bytes('''
        <typesystem package="PySide6.QtXml">
            <value-type name="QDomDocument">
        </typesystem>
        ''', "UTF-8"))

    def tearDown(self):
        del self.dom
        del self.goodXmlData
        del self.badXmlData
        # PYSIDE-535: Need to collect garbage in PyPy to trigger deletion
        gc.collect()

    def testQDomDocumentSetContentWithBadXmlData(self):
        '''Sets invalid xml as the QDomDocument contents.'''
        parseResult = self.dom.setContent(self.badXmlData,
                                          QDomDocument.ParseOption.UseNamespaceProcessing)
        self.assertFalse(parseResult)
        self.assertEqual(parseResult.errorMessage, 'Opening and ending tag mismatch.')
        self.assertEqual(parseResult.errorLine, 4)

    def testQDomDocumentSetContentWithGoodXmlData(self):
        '''Sets valid xml as the QDomDocument contents.'''
        parseResult = self.dom.setContent(self.goodXmlData,
                                          QDomDocument.ParseOption.UseNamespaceProcessing)
        self.assertTrue(parseResult)
        self.assertEqual(parseResult.errorMessage, '')
        self.assertEqual(parseResult.errorLine, 0)
        self.assertEqual(parseResult.errorColumn, 0)

    def testQDomDocumentData(self):
        '''Checks the QDomDocument elements for the valid xml contents.'''

        def checkAttribute(element, attribute, value):
            self.assertTrue(isinstance(root, QDomElement))
            self.assertFalse(element.isNull())
            self.assertTrue(element.hasAttribute(attribute))
            self.assertEqual(element.attribute(attribute), value)

        parseResult = self.dom.setContent(self.goodXmlData,  # noqa F:841
                                          QDomDocument.ParseOption.UseNamespaceProcessing)
        root = self.dom.documentElement()
        self.assertEqual(root.tagName(), 'typesystem')
        checkAttribute(root, 'package', 'PySide6.QtXml')

        child = root.firstChildElement('value-type')
        checkAttribute(child, 'name', 'QDomDocument')

        child = child.nextSiblingElement('value-type')
        checkAttribute(child, 'name', 'QDomElement')


if __name__ == '__main__':
    unittest.main()
