The Qt Charts module provides a set of easy-to-use chart components. It uses
the Qt Graphics View Framework to integrate charts with modern user interfaces.
Qt Charts can be used as QWidgets,
:class:`QGraphicsWidget<PySide6.QtWidgets.QGraphicsWidget>` , or QML types.
Users can easily create impressive charts by selecting one of the themes.

Getting Started
^^^^^^^^^^^^^^^

To include the definitions of modules classes, use the following
directive:

    ::

        from PySide6 import QtCharts

.. note:: An instance of QApplication is required for the QML types as the
   module depends on Qt's \l{Graphics View Framework} for rendering.
   QGuiApplication is not sufficient.
