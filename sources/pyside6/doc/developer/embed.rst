.. _python-file-embedding:

Python File Embedding
=====================

``libshiboken`` needs a set of Python helper files at runtime to provide
signature introspection, ``help()`` output, IDE autocompletion, and
informative error messages for PySide6 wrapped types. Rather than installing
these as loose ``.py`` files alongside the binary, they are baked directly
into ``libshiboken`` at build time.

The ``sources/shiboken6/libshiboken/embed/`` folder contains the two files
responsible for this mechanism.

Embed folder contents
---------------------

embedding_generator.py
^^^^^^^^^^^^^^^^^^^^^^

A build-time script invoked by CMake. It takes the Python helper files from
``sources/shiboken6/shibokenmodule/files.dir/shibokensupport/``, packs them
into a ZIP archive, encodes the result as base64, and writes it into a
generated C++ header file ``signature_inc.h``. It also embeds
``signature_bootstrap.py`` as bytecode into a second header,
``signature_bootstrap_inc.h``. Both headers are then compiled into
``libshiboken``.

signature_bootstrap.py
^^^^^^^^^^^^^^^^^^^^^^

A Python script that runs at runtime, the first time any PySide6 module is
imported. It decodes the ZIP archive from memory, registers a custom import
finder, and makes the helper files available to Python's import system
without any disk access.

Modifying the helper files
--------------------------

The source files that get embedded live under::

    sources/shiboken6/shibokenmodule/files.dir/shibokensupport/

Edit them there and rebuild. CMake re-runs ``embedding_generator.py``
automatically when any of those files change.

Debugging without rebuilding
----------------------------

Set the ``SBK_EMBED`` environment variable to ``0`` before running your
script. This makes ``libshiboken`` extract the embedded files to a
``files.dir/`` directory on disk instead of running them from memory.
Files in that directory can be edited and changes take effect on the next
run without a rebuild.

.. note::
    To go back to embedded mode, set ``SBK_EMBED=1`` and run once - this
    deletes the ``files.dir`` folder and the binary returns to running the
    files from memory. Running with ``SBK_EMBED=0`` outside of a development
    environment is not recommended.
