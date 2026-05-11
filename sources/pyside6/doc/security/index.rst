.. _Security-Considerations:

Security Considerations
=======================

This page lists some topics relevant in context of the upcoming
`CRA`_ regulation in the EU.

Deployment
----------

Getting your projects installed on other computers or people is a task most
Python developers would face at some point. When trying a local copy of the
Python files, you need to be certain that the source code hasn't been tampered
with or maliciously modified. For that reason, we recommend that, for the
distribution of PySide projects, you always deploy them. Please check our
section on :ref:`deployment-guides`, where you can find how to do this using
:ref:`pyside6-deploy` or other tools.

The Python Interpreter
----------------------

The `CRA`_ does not include the Python interpreter, since that would be
`very problematic`_\, but there is an exception for non-commercial
Open Source software. Because of that, the security scope of Qt for Python
as an offering does not include the interpreter the applications are using.

Security-relevant Topics in Qt for Python
-----------------------------------------

* `Shiboken.VoidPtr`_
* :func:`PySide6.QtUiTools.loadUiType`
* :ref:`Qt Widgets Designer Custom Widgets<designer-tool-custom-widgets>`
* :ref:`pyobject-serialization`

.. _pyobject-serialization:

Python Object Serialization in Qt Data Streams
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PySide6 can store Python objects as arguments of queued signal connections or as values written to
:class:`~PySide6.QtCore.QSettings`. Internally, PySide6 serializes them using Python's pickle module
into a :class:`~PySide6.QtCore.QDataStream` byte sequence.

**Only Python builtin types can be read back.** Deserialization is restricted
to ``dict``, ``list``, ``tuple``, ``set``, ``frozenset``, ``str``, ``int``,
``float``, ``bool``, ``bytes``, ``bytearray``, and ``complex``. Attempting to
deserialize any other type raises a ``RuntimeError``.

This restriction prevents an attacker who can supply a crafted data stream (for
example via a :mod:`~PySide6.QtRemoteObjects` connection or a tampered settings file) from
achieving remote code execution, while still supporting the common use cases of
storing plain data structures in :class:`~PySide6.QtCore.QSettings`.

When a :class:`~PySide6.QtCore.QDataStream` containing an unsupported Python object type is read,
the following happens:

* :meth:`~PySide6.QtCore.QSettings.value` raises a ``RuntimeError``.
* :mod:`~PySide6.QtRemoteObjects` marks the stream as corrupt and drops the connection.

.. warning::

    Do not pass custom Python class instances to :meth:`~PySide6.QtCore.QSettings.setValue` or
    use them as :mod:`~PySide6.QtRemoteObjects` property values. Writing such objects
    succeeds (serialization is unrestricted), but reading them back will raise
    a ``RuntimeError``. Use only the builtin types listed above, or serialize
    your custom objects to a builtin representation (e.g. a ``dict``) before
    storing.

Security in Qt
--------------

* :ref:`Security-in-Qt`
* :ref:`Qt-Shared-Security-Model`
* :ref:`overviews_untrusted-data`

.. _`Shiboken.VoidPtr`: https://doc.qt.io/qtforpython-6/shiboken6/shibokenmodule.html#Shiboken.VoidPtr
.. _`CRA`: https://www.qt.io/cyber-resilience-act
.. _`very problematic`: https://pyfound.blogspot.com/2023/04/the-eus-proposed-cra-law-may-have.html
