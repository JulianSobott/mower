"""
:module: mower.
:synopsis:
:author: Julian Sobott
:author: 

public functions
-----------------

.. autofunction:: XXX

public classes
-----------------

.. autoclass:: XXX
    :members:


private functions
------------------

.. autofunction:: XXX

private classes
-----------------

.. autoclass:: XXX
    :members:

"""
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQuick import QQuickView
from PyQt5 import QtQml
import sys

# app = QApplication(sys.argv)
# engine = QtQml.QQmlApplicationEngine("control_window.qml")
# engine.quit.connect(app.quit)
# sys.exit(app.exec_())




app = QApplication(sys.argv)
view = QQuickView()
view.setSource(QUrl("control_window.qml"))
view.show()
sys.exit(app.exec_())
