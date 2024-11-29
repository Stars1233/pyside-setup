Calling Python Methods from QML
===============================

Introduce how to invoke Python methods (slots) from QML.

**Key Features:**

- **Python Class with Slots:** Defines a Console class in Python with multiple slots using the
  :deco:`~PySide6.QtCore.Slot` decorator.
- **Exposing Python Class to QML:** Uses :deco:`~PySide6.QtQml.QmlElement` to make the Console class
  available in QML.
- **Calling Slots from QML:** In QML, instantiates Console and calls its methods in response to user
  interactions.
