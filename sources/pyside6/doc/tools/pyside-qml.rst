.. _pyside6-qml:

pyside6-qml
===========

``pyside6-qml``  mimics some capabilities of Qt's `qml`_ runtime utility by directly
invoking QQmlEngine/QQuickView. It enables prototyping with QML/QtQuick without the need to write
any Python code that loads the QML files either through `QQmlApplicationEngine`_ or
the `QQuickView`_ class. The tool also detects the QML classes implemented in Python
and registers them with the QML type system.

Usage
-----

Consider the example `Extending QML - Plugins Example`_. This example does
not have a Python file with a ``main`` function that initializes a QmlEngine to load the QML file
``app.qml``. You can run the example by running

.. code-block:: bash

    pyside6-qml examples/qml/tutorials/extending-qml/chapter6-plugins/app.qml -I examples/qml/tutorials/extending-qml/chapter6-plugins/Charts

The ``-I`` flag is used to point ``pyside6-qml`` to the folder containing Python files that
implement QML classes.

Command Line Options
--------------------

Here are all the command line options of ``pyside6-qml``:

Arguments
^^^^^^^^^

* **file**: This option refers to the QML file to be loaded by ``pyside6-qml``. This option does not
  have a name or a flag. Therefore, this option should be the first option supplied to
  ``pyside6-qml``. For example,

.. code-block:: bash

    pyside6-qml /path/to/test.qml

Options
^^^^^^^

* **--module-paths/-I**: Specify space-separated folder/file paths which point to the Python files
  that implement QML classes. By default, the parent directory of the QML file supplied to
  ``pyside6-qml`` is searched recursively for all Python files and they are imported. Otherwise,
  only the paths given in module paths are searched.

* **--verbose/-v**: Run ``pyside6-qml`` in verbose mode. When run in this mode, pyside6-qml prints
  log messages during various stages of processing.

Options that align with the `qml`_ runtime utility
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

* **--app-typ/-a**: Specifies which application class to use. It takes one of the three values -
  ``core, gui, widget``. The default value is *gui*.

* **--config/-c**: Load the given built-in configuration. It takes one of two values - ``default,
  resizeToItem``. This option is only relevant for a QtQuick application. If ``default`` is used,
  the view resizes to the size of the root item in the QML. If ``resizeToItem`` is used, the view
  automatically resizes the root item to the size of the view.

* **--list-conf**: List the built-in configurations. ``pyside6-qml`` has two built-in configurations
  - ``default`` and ``resizeToItem``. See the option ``--config`` for more information.

* **--rhi/-r**: Specifies the backend for the Qt graphics abstraction (RHI). It takes one of the
  four values - ``vulkan, metal, d3dll, gl``.

* **--verbose/-v**: List the built-in configurations. ``pyside6-qml`` has two built-in
  configurations - *default* and *resizeToItem*. See the option ``--config`` for more information.

* **--gles**: Force use of GLES (AA_UseOpenGLES).

* **--desktop**: Force use of desktop OpenGL (AA_UseDesktopOpenGL).

* **--software**: Force use of software rendering(AA_UseSoftwareOpenGL).

* **--disable-context-sharing**: Disable the use of a shared GL context for QtQuick Windows".

Security Considerations
-----------------------

``pyside6-qml`` automatically imports every Python file it finds in the QML file's
parent directory (or under the paths given with ``-I``/``--module-paths``) and
executes them in the current process.  This is by design: QML elements backed by
Python classes must be registered before the QML engine loads the file.

Because of this, **treat a QML project the same way you would treat a Python
project**: do not run ``pyside6-qml`` on files from an untrusted source unless you
are willing to execute the accompanying Python code with your own privileges.  In
particular, be cautious when:

- opening QML files received by e-mail, downloaded from the internet, or checked
  out from an unfamiliar repository, or
- running ``pyside6-qml`` inside a CI pipeline on code submitted by external
  contributors.

.. _`qml`: https://doc.qt.io/qt-6/qtquick-qml-runtime.html
.. _`QQmlApplicationEngine`: https://doc.qt.io/qt-6/qqmlapplicationengine.html
.. _`QQuickView`: https://doc.qt.io/qt-6/qquickview.html
.. _`Extending QML - Plugins Example`: https://doc.qt.io/qtforpython-6/examples/example_qml_tutorials_extending-qml_chapter6-plugins.html
