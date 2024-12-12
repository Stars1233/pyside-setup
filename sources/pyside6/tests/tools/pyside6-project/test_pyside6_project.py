# Copyright (C) 2024 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only
import contextlib
import io
import os
import shutil
import sys
import unittest
from unittest import mock
from unittest import TestCase
import tempfile
import importlib
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from init_paths import init_test_paths

init_test_paths(False)


class PySide6ProjectTestBase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pyside_root = Path(__file__).parents[5].resolve()
        cls.example_root = cls.pyside_root / "examples"
        tools_path = cls.pyside_root / "sources" / "pyside-tools"
        if tools_path not in sys.path:
            sys.path.append(str(tools_path))
        cls.project = importlib.import_module("project")
        cls.project_lib = importlib.import_module("project_lib")
        cls.temp_dir = Path(tempfile.mkdtemp())
        cls.current_dir = Path.cwd()
        # print no outputs to stdout
        sys.stdout = mock.MagicMock()

    @classmethod
    def tearDownClass(cls):
        os.chdir(cls.current_dir)
        shutil.rmtree(cls.temp_dir)

    def setUp(self):
        os.chdir(self.temp_dir)


class TestPySide6ProjectDesignStudio(PySide6ProjectTestBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        example_drumpad = Path(__file__).parent / "example_drumpad"
        cls.temp_example_drumpad = Path(
            shutil.copytree(example_drumpad, cls.temp_dir / "drumpad")
        ).resolve()

    def testDrumpadExample(self):
        # This test compiles the .qrc file into a .py file and checks whether the compilation is
        # carried out only when required
        compiled_resources_path = self.temp_example_drumpad / "Python" / "autogen" / "resources.py"
        resources_path = self.temp_example_drumpad / "Drumpad.qrc"
        requires_rebuild = self.project_lib.utils.requires_rebuild

        self.assertFalse(compiled_resources_path.exists())

        os.chdir(self.temp_example_drumpad / "Python")
        self.project.main(mode="build")

        self.assertTrue(compiled_resources_path.exists())
        self.assertFalse(requires_rebuild([resources_path], compiled_resources_path))

        # Refresh the modification timestamp of the .qrc resources file so that it is considered
        # as modified
        resources_path.touch()

        self.assertTrue(requires_rebuild([resources_path], compiled_resources_path))

        self.project.main(mode="build")

        self.assertFalse(requires_rebuild([resources_path], compiled_resources_path))

        # Refresh the modification timestamp of one of the resources files
        list((self.temp_example_drumpad / "Resources").glob("*.txt"))[0].touch()
        self.assertTrue(requires_rebuild([resources_path], compiled_resources_path))

        self.project.main(mode="clean")

        self.assertFalse(compiled_resources_path.exists())


class TestPySide6ProjectNew(PySide6ProjectTestBase):
    def testNewUi(self):
        with self.assertRaises(SystemExit) as context:
            self.project.main(mode="new-ui", file="TestProject")
        test_project_path = Path("TestProject")
        self.assertTrue((test_project_path / "TestProject.pyproject").exists())
        self.assertTrue((test_project_path / "mainwindow.ui").exists())
        self.assertTrue((test_project_path / "main.py").exists())
        self.assertEqual(context.exception.code, 0)
        shutil.rmtree(test_project_path)

    def testRaiseErrorOnExistingProject(self):
        with self.assertRaises(SystemExit) as context:
            self.project.main(mode="new-ui", file="TestProject")
        self.assertEqual(context.exception.code, 0)
        error_message = io.StringIO()
        with self.assertRaises(SystemExit) as context, contextlib.redirect_stderr(error_message):
            self.project.main(mode="new-ui", file="TestProject")
        self.assertEqual(context.exception.code, -1)
        self.assertTrue(error_message.getvalue())  # some error message is printed
        shutil.rmtree(self.temp_dir / "TestProject")

    def testNewQuick(self):
        with self.assertRaises(SystemExit) as context:
            self.project.main(mode="new-quick", file="TestProject")
        test_project_path = Path("TestProject")
        self.assertTrue((test_project_path / "TestProject.pyproject").exists())
        self.assertTrue((test_project_path / "main.qml").exists())
        self.assertTrue((test_project_path / "main.py").exists())
        self.assertEqual(context.exception.code, 0)
        shutil.rmtree(test_project_path)

    def testNewWidget(self):
        with self.assertRaises(SystemExit) as context:
            self.project.main(mode="new-widget", file="TestProject")
        test_project_path = Path("TestProject")
        self.assertTrue((test_project_path / "TestProject.pyproject").exists())
        self.assertTrue((test_project_path / "main.py").exists())
        self.assertEqual(context.exception.code, 0)
        shutil.rmtree(test_project_path)

    def testRaiseErrorWhenNoProjectNameIsSpecified(self):
        error_message = io.StringIO()
        with self.assertRaises(SystemExit) as context, contextlib.redirect_stderr(error_message):
            self.project.main(mode="new-widget", file="")
        self.assertEqual(context.exception.code, 1)
        self.assertTrue(error_message.getvalue())  # some error message is printed


class TestPySide6ProjectRun(PySide6ProjectTestBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        example_widgets = cls.example_root / "widgets" / "widgets" / "tetrix"
        cls.temp_example_tetrix = Path(
            shutil.copytree(example_widgets, Path(cls.temp_dir) / "tetrix")
        ).resolve()

    def testRunEmptyProject(self):
        project_folder = self.temp_dir / "TestProject"
        project_folder.mkdir()
        os.chdir(project_folder)
        error_message = io.StringIO()
        with self.assertRaises(SystemExit) as context, contextlib.redirect_stderr(error_message):
            self.project.main(mode="run")
        self.assertEqual(context.exception.code, 1)
        self.assertTrue(error_message.getvalue())  # some error message is printed


if __name__ == "__main__":
    unittest.main()
