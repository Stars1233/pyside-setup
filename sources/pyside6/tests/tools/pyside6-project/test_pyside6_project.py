# Copyright (C) 2024 The Qt Company Ltd.
# SPDX-License-Identifier: LicenseRef-Qt-Commercial OR LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only
from __future__ import annotations

import contextlib
import difflib
import importlib
import io
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import TestCase
from unittest import mock
from unittest.mock import patch

sys.path.append(str(Path(__file__).resolve().parents[2]))
from init_paths import init_test_paths

init_test_paths(False)


def file_diff(expected_file: Path, actual_file: Path) -> str:
    """
    Get a unified diff between two files
    """
    target_text = expected_file.read_text(encoding="utf-8").splitlines()
    generated_text = actual_file.read_text(encoding="utf-8").splitlines()

    return "\n".join(difflib.unified_diff(
        generated_text, target_text,
        fromfile=str(actual_file),
        tofile=str(expected_file),
        lineterm=""
    ))


class PySide6ProjectTestBase(TestCase):
    # If a project name is specified, on each the test, the project folder will be copy to the
    # temp dir and the current dir will be changed to the project folder
    # The project name must match an existing folder in the folder where this file is located
    project_name: str | None = None

    @classmethod
    def setUpClass(cls):
        cls.pyside_root = Path(__file__).parents[5].resolve()
        tools_path = cls.pyside_root / "sources" / "pyside-tools"
        if tools_path not in sys.path:
            sys.path.append(str(tools_path))
        cls.project = importlib.import_module("project")
        cls.project_lib = importlib.import_module("project_lib")
        cls.temp_dir = Path(tempfile.mkdtemp())
        cls.current_dir = Path.cwd()
        # print no outputs to stdout
        sys.stdout = mock.MagicMock()
        if cls.project_name:
            cls.temp_project = Path(cls.temp_dir / cls.project_name).resolve()
        os.chdir(cls.temp_dir)

    def setUp(self):
        super().setUp()
        if self.project_name:
            shutil.copytree(Path(__file__).parent / self.project_name, self.temp_project)
            os.chdir(self.temp_project)

    def tearDown(self):
        super().tearDown()
        if self.project_name:
            os.chdir(self.temp_dir)
            shutil.rmtree(self.temp_project)

    @classmethod
    def tearDownClass(cls):
        os.chdir(cls.current_dir)
        shutil.rmtree(cls.temp_dir)


class TestPySide6ProjectDesignStudio(PySide6ProjectTestBase):
    project_name = "example_drumpad"

    def testDrumpadExample(self):
        # This test compiles the .qrc file into a .py file and checks whether the compilation is
        # carried out only when required
        compiled_resources_path = Path("Python") / "autogen" / "resources.py"
        resources_path = Path("Drumpad.qrc")

        requires_rebuild = self.project_lib.utils.requires_rebuild
        pyproject_path = Path("Python") / "Drumpad.pyproject"
        self.assertFalse(compiled_resources_path.exists())
        self.assertTrue(pyproject_path.exists())
        self.project.main(mode="build", project_path=pyproject_path)

        self.assertTrue(compiled_resources_path.exists())
        self.assertFalse(requires_rebuild([resources_path], compiled_resources_path))

        # Refresh the modification timestamp of the .qrc resources file so that it is considered
        # as modified
        resources_path.touch()

        self.assertTrue(requires_rebuild([resources_path], compiled_resources_path))

        self.project.main(mode="build", project_path=pyproject_path)

        self.assertFalse(requires_rebuild([resources_path], compiled_resources_path))

        # Refresh the modification timestamp of one of the resources files
        list((Path("Resources").glob("*.txt")))[0].touch()
        self.assertTrue(requires_rebuild([resources_path], compiled_resources_path))

        self.project.main(mode="clean", project_path=pyproject_path)

        self.assertFalse(compiled_resources_path.exists())

    def testMigrateDrumpadExample(self):
        # The pyproject.toml file already contains the expected output
        expected_pyproject_toml = Path("Python") / "pyproject.toml"
        expected_pyproject_toml.rename(expected_pyproject_toml.parent / "expected_pyproject.toml")
        existing_pyproject = Path("Python") / "Drumpad.pyproject"

        with self.assertRaises(SystemExit) as context:
            with patch("builtins.input", return_value="y"):
                self.project.main(mode="migrate-pyproject",
                                  project_path=existing_pyproject.as_posix())

        self.assertEqual(0, context.exception.code)
        generated_pyproject_toml = Path("Python") / "pyproject.toml"
        self.assertTrue(generated_pyproject_toml.exists())
        diff = file_diff(expected_pyproject_toml, generated_pyproject_toml)
        self.assertFalse(diff, f"Generated pyproject.toml does not match:\n{diff}")


class TestPySide6ProjectNew(PySide6ProjectTestBase):
    def testNewUi(self):
        test_project_path = self.temp_dir / "NewUiProject"
        with self.assertRaises(SystemExit) as context:
            self.project.main(mode="new-ui", project_dir=test_project_path.as_posix())

        self.assertTrue((test_project_path / "pyproject.toml").exists())
        self.assertTrue((test_project_path / "mainwindow.ui").exists())
        self.assertTrue((test_project_path / "main.py").exists())
        self.assertEqual(0, context.exception.code)
        shutil.rmtree(test_project_path)

    def testRaiseErrorOnExistingNonEmptyProject(self):
        # Create a project twice to ensure that an error is raised
        project_name = "TestProject"
        with self.assertRaises(SystemExit) as context:
            self.project.main(mode="new-ui", project_dir=project_name)

        self.assertEqual(0, context.exception.code)

        error_message = io.StringIO()
        with self.assertRaises(SystemExit) as context:
            with contextlib.redirect_stderr(error_message):
                self.project.main(mode="new-ui", project_dir=project_name)

        self.assertEqual(1, context.exception.code)
        self.assertTrue(f"Can not create project at {project_name}: directory is not empty." in
                        error_message.getvalue())
        shutil.rmtree(self.temp_dir / "TestProject")

    def testRaiseErrorOnInvalidProjectName(self):
        # Create a project with an empty project name
        error_message = io.StringIO()
        with self.assertRaises(SystemExit) as context:
            with contextlib.redirect_stderr(error_message):
                self.project.main(mode="new-ui", project_dir="asdf/?^%$#@!")

        self.assertEqual(1, context.exception.code)
        self.assertTrue("Invalid project name" in error_message.getvalue())

    def testNewQuick(self):
        test_project_path = Path("QuickProject")

        with self.assertRaises(SystemExit) as context:
            self.project.main(mode="new-quick", project_dir=str(test_project_path))

        self.assertTrue((test_project_path / "pyproject.toml").exists())
        self.assertTrue((test_project_path / "main.qml").exists())
        self.assertTrue((test_project_path / "main.py").exists())
        self.assertEqual(0, context.exception.code)
        shutil.rmtree(test_project_path)

    def testNewWidget(self):
        project_dir = self.temp_dir / "inner_folder" / "another_folder" / "WidgetProject"
        with self.assertRaises(SystemExit) as context:
            self.project.main(mode="new-widget", project_dir=project_dir.as_posix())
        self.assertTrue((project_dir / "pyproject.toml").exists())
        self.assertTrue((project_dir / "main.py").exists())
        self.assertEqual(0, context.exception.code)
        shutil.rmtree(project_dir)

    def testRaiseErrorWhenNoProjectNameIsSpecified(self):
        mode = "new-widget"
        error_message = io.StringIO()
        with self.assertRaises(SystemExit) as context, contextlib.redirect_stderr(error_message):
            self.project.main(mode=mode)
        self.assertEqual(context.exception.code, 1)
        expected_msg = f"Error creating new project: {mode} requires a directory name or path"
        self.assertTrue(expected_msg in error_message.getvalue())

    def testCreateProjectLegacyPyProjectFile(self):
        project_path = Path("TestPyProjectJSON")
        mode = "new-widget"
        with self.assertRaises(SystemExit) as context:
            self.project.main(mode=mode, project_dir=project_path.as_posix(), legacy_pyproject=True)
        self.assertEqual(0, context.exception.code)
        self.assertTrue((project_path / "main.py").exists())
        self.assertTrue((project_path / f"{project_path.name}.pyproject").exists())


class TestPySide6ProjectRun(PySide6ProjectTestBase):
    project_name = "example_project"

    def testRaiseErrorWhenRunningEmptyProject(self):
        # Create a new empty project in the temp dir
        project_folder = self.temp_dir / "empty_project"
        project_folder.mkdir()
        os.chdir(project_folder)

        error_message = io.StringIO()
        with self.assertRaises(SystemExit) as context:
            with contextlib.redirect_stderr(error_message):
                self.project.main(mode="run")

        os.chdir(self.temp_dir)
        shutil.rmtree(project_folder)

        self.assertEqual(1, context.exception.code)
        self.assertTrue("No project file found" in error_message.getvalue())

    def testRunExampleProject(self):
        # The project is executed in a subprocess. The proejct code reads the PYSIDE_TESTING
        # environment variable to avoid starting the Qt event loop
        os.environ["PYSIDE_TESTING"] = "1"
        with self.assertRaises(SystemExit) as context:
            self.project.main(mode="run")
        os.environ.pop("PYSIDE_TESTING")
        self.assertEqual(0, context.exception.code)

        self.assertEqual(Path("pyproject.toml").resolve(),
                         self.project_lib.resolve_valid_project_file())


class TestPySide6ProjectExampleProject(PySide6ProjectTestBase):
    """
    Test of an example project with both pyproject.toml and .pyproject valid files.
    Contains a subproject with its own pyproject.toml file and .pyproject file too
    """
    project_name = "example_project"

    def testMigratePyProjectToToml(self):
        # The existing pyproject.toml file contains the expected output
        expected_pyproject_toml = Path("pyproject.toml").rename("expected_pyproject.toml")
        expected_subproject_pyproject_toml = Path("subproject") / "pyproject.toml"
        expected_subproject_pyproject_toml.rename(
            expected_subproject_pyproject_toml.parent / "expected_subproject_pyproject.toml")

        with self.assertRaises(SystemExit) as context:
            self.project.main(mode="migrate-pyproject")

        self.assertEqual(0, context.exception.code)

        generated_pyproject_toml = Path("pyproject.toml")
        self.assertTrue(generated_pyproject_toml.exists())
        diff = file_diff(expected_pyproject_toml, generated_pyproject_toml)
        self.assertFalse(diff, f"Generated pyproject.toml does not match:\n{diff}")

        generated_subproject_pyproject_toml = Path("subproject") / "pyproject.toml"
        self.assertTrue(generated_subproject_pyproject_toml.exists())
        diff = file_diff(expected_subproject_pyproject_toml, generated_subproject_pyproject_toml)
        self.assertFalse(diff, f"Generated subproject/pyproject.toml does not match:\n{diff}")

    def testMigratePyProjectToTomlSpecifyingPyProjectFile(self):
        # The existing pyproject.toml file contains the expected output
        existing_pyproject = Path("example_project.pyproject")
        expected_pyproject_toml = Path("pyproject.toml")
        expected_pyproject_toml.rename("example_project.toml")

        expected_subproject_pyproject_toml = Path("subproject") / "pyproject.toml"
        expected_subproject_pyproject_toml.rename(
            expected_subproject_pyproject_toml.parent / "expected_pyproject.toml")

        with self.assertRaises(SystemExit) as context:
            with patch("builtins.input", return_value="y"):
                self.project.main(mode="migrate-pyproject",
                                  project_path=existing_pyproject.as_posix())

        self.assertEqual(0, context.exception.code)

        generated_pyproject_toml = Path("pyproject.toml")
        self.assertTrue(generated_pyproject_toml.exists())
        diff = file_diff(expected_pyproject_toml, generated_pyproject_toml)
        self.assertFalse(diff, f"Generated pyproject.toml does not match:\n{diff}")

        generated_subproject_pyproject_toml = Path("subproject") / "pyproject.toml"
        self.assertTrue(generated_subproject_pyproject_toml.exists())
        diff = file_diff(expected_subproject_pyproject_toml, generated_subproject_pyproject_toml)
        self.assertFalse(diff, f"Generated subproject/pyproject.toml does not match:\n{diff}")


class TestPySide6ProjectExistingPyProjectToml(PySide6ProjectTestBase):
    """
    Test for migrating a project with an existing pyproject.toml file which does not contain the
    [tool.pyside6-project] section
    """
    project_name = "existing_pyproject_toml"

    def testMigratePyProjectToTomlAlreadyExistingTomlFile(self):
        with self.assertRaises(SystemExit) as context:
            with patch("builtins.input", return_value="y"):
                self.project.main(mode="migrate-pyproject")

        self.assertEqual(0, context.exception.code)
        diff = file_diff(Path("expected_pyproject.toml"),
                         Path("pyproject.toml"))
        self.assertFalse(diff, f"Updated pyproject.toml does not match:\n{diff}")


class TestPySide6ProjectInvalidPyProjectToml(PySide6ProjectTestBase):
    """
    Check the current behavior in a project with an existing invalid pyproject.toml file and
    invalid_pyproject.pyproject file
    """

    project_name = "invalid_pyproject"

    def testRunInvalidPyProjectTomlFile(self):
        pyproject_toml = Path("pyproject.toml")
        self.assertTrue(pyproject_toml.exists())
        self.assertTrue(self.project_lib.parse_pyproject_toml(pyproject_toml).errors)

        error_message = io.StringIO()
        with contextlib.redirect_stderr(error_message):
            with self.assertRaises(SystemExit) as context:
                self.project.main(mode="run", project_path=pyproject_toml.as_posix())

        self.assertEqual(1, context.exception.code)
        self.assertTrue("Invalid project file" in error_message.getvalue())

    def testRunSpecifyingPyProjectJsonFile(self):
        # Check that the *.pyproject file is used if the pyproject.toml is invalid when using
        # pyside6-project run

        pyproject_toml_file = Path("pyproject.toml")
        self.assertTrue(pyproject_toml_file.exists())
        # Ensure that pyproject.toml is considered invalid
        self.assertTrue(self.project_lib.parse_pyproject_toml(pyproject_toml_file).errors)

        valid_pyproject = Path("valid_pyproject.pyproject")
        self.assertTrue(valid_pyproject.exists())

        # Ensure that the project can still be run specifying a valid *.pyproject JSON file
        with self.assertRaises(SystemExit) as context:
            self.project.main(mode="run", project_path=valid_pyproject.as_posix())

        self.assertEqual(0, context.exception.code)
        self.assertTrue(Path("main.py").exists())

    def testErrorRaisesWhenRunningWithoutSpecifyingProjectFile(self):
        # The project folder contains two *.pyproject JSON files.
        # The tool should raise an error because the project file is not specified
        error_message = io.StringIO()
        with contextlib.redirect_stderr(error_message):
            with self.assertRaises(SystemExit) as context:
                self.project.main(mode="run")
        self.assertEqual(1, context.exception.code)
        self.assertTrue("Multiple project files found" in error_message.getvalue())

    def testRaiseErrorResolvingInvalidProjectFile(self):
        # Simulate that the user is specifying an invalid project file
        invalid_pyproject_file = Path("invalid_pyproject.pyproject")
        self.assertTrue(invalid_pyproject_file.exists())

        with self.assertRaises(ValueError) as context:
            self.project_lib.resolve_valid_project_file(invalid_pyproject_file.as_posix())

        exception_message = str(context.exception)
        self.assertTrue("Invalid project file" in exception_message)
        self.assertTrue(str(invalid_pyproject_file) in exception_message)

    def testResolveValidProjectFile(self):
        # Simulate that the user is specifying a valid project file
        valid_pyproject_file = Path("valid_pyproject.pyproject")
        actual_project_file = self.project_lib.resolve_valid_project_file(
            valid_pyproject_file.as_posix())
        self.assertEqual(valid_pyproject_file.resolve(), actual_project_file)

    def testRaiseErrorResolvingInvalidPyProjectToml(self):
        # Simulate that the user is specifying an invalid pyproject.toml file
        pyproject_toml_file = Path("pyproject.toml")
        self.assertTrue(pyproject_toml_file.exists())

        with self.assertRaises(ValueError) as context:
            self.project_lib.resolve_valid_project_file(pyproject_toml_file.as_posix())

        exception_message = str(context.exception)
        self.assertTrue("Invalid project file" in exception_message)
        self.assertTrue(str(pyproject_toml_file) in exception_message)

    def testMigrateInvalidPyProjectToml(self):
        # Can not migrate a project with an invalid pyproject.toml file
        error_message = io.StringIO()
        with contextlib.redirect_stderr(error_message):
            with self.assertRaises(SystemExit) as context:
                with patch("builtins.input", return_value="y"):
                    self.project.main(mode="migrate-pyproject")

        self.assertEqual(1, context.exception.code)
        self.assertTrue("Invalid project file" in error_message.getvalue())

    def testMigrateInvalidPyProjectTomlSpecifyingWrongFile(self):
        # Test specifying the pyproject.toml file as the project file to be migrated
        existing_invalid_pyproject_toml = Path("pyproject.toml")
        self.assertTrue(
            bool(self.project_lib.parse_pyproject_toml(existing_invalid_pyproject_toml).errors))

        error_message = io.StringIO()
        with contextlib.redirect_stderr(error_message):
            with self.assertRaises(SystemExit) as context:
                self.project.main(mode="migrate-pyproject",
                                  project_path=existing_invalid_pyproject_toml)

        self.assertEqual(1, context.exception.code)
        self.assertTrue("Cannot migrate non \"*.pyproject\" file" in error_message.getvalue())
        self.assertTrue("pyproject.toml" in error_message.getvalue())


def testRunInvalidPyProjectToml(self):
    # Ensure that the .pyproject file is preferred over the invalid pyproject.toml file.
    # This preserves the backward compatibility of the .pyproject file

    # Remove the invalid invalid_pyproject.pyproject file first
    Path("invalid_pyproject.pyproject").unlink()
    self.assertFalse(Path("invalid_pyproject.pyproject").exists())

    with self.assertRaises(SystemExit) as context:
        self.project.main(mode="run")

    self.assertEqual(0, context.exception.code)
    self.assertEqual(Path("valid_pyproject.pyproject").resolve(),
                     self.project_lib.resolve_valid_project_file())


class TestPySide6ProjectMultiplePyProject(PySide6ProjectTestBase):
    project_name = "multiple_pyproject"

    def testCancelMigration(self):
        # Ensure that the pyproject.toml is not created if the user cancels the operation
        with self.assertRaises(SystemExit) as context:
            with patch("builtins.input", return_value="n"):
                self.project.main(mode="migrate-pyproject")

        self.assertEqual(0, context.exception.code)
        self.assertFalse(Path("pyproject.toml").exists())

    def testMigrateMultiplePyProjectFilesToToml(self):
        expected_pyproject_toml = Path("expected_pyproject.toml")
        generated_pyproject_toml = Path("pyproject.toml")

        with self.assertRaises(SystemExit) as context:
            with patch("builtins.input", return_value="y"):
                self.project.main(mode="migrate-pyproject")

        self.assertEqual(0, context.exception.code)
        self.assertTrue(generated_pyproject_toml.exists())
        diff = file_diff(expected_pyproject_toml, generated_pyproject_toml)
        self.assertFalse(diff, f"Generated pyproject.toml does not match:\n{diff}")


if __name__ == "__main__":
    unittest.main()
