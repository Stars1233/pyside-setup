The Qt Qml module implements the QML language and offers APIs to register types
for it.

The Qt Qml module provides a framework for developing applications and
libraries with the :ref:`The-QML-Reference` . It defines and implements the
language and engine infrastructure, and provides an API to enable application
developers to register custom QML types and modules and integrate QML code with
JavaScript and Python. The Qt Qml module provides both a QML API a Python API.

Using the Module
^^^^^^^^^^^^^^^^

To include the definitions of modules classes, use the following
directive:

::

    import PySide6.QtQml

Registering QML Types and QML Modules
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

See :ref:`tutorial_qmlintegration`.

Tweaking the engine
^^^^^^^^^^^^^^^^^^^

There are a number of knobs you can turn to customize the behavior of the QML
engine. The page on :ref:`Configuring-the-JavaScript-Engine` lists the
environment variables you may use to this effect. The description of
:ref:`The-QML-Disk-Cache` describes the options related to how your QML
components are compiled and loaded.
