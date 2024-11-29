Receiving return values from Python in QML
==========================================

Demonstrate how to call Python methods from QML that return values.

**Key Features:**

- **Python Class with Returning Slot:** Defines a `RotateValue` class with a slot that returns an
  integer.
- **Exposing Class to QML:** Uses :deco:`~PySide6.QtQml.QmlElement` to expose RotateValue to QML.
- **Using Return Values in QML:** Calls the Python method from QML and uses the returned value to
  update the UI.
