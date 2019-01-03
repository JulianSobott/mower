"""
@author: Julian Sobott
@created: XX.XX.2018
@brief:
@description:

@external_use:

@internal_use:

"""
from PyQt5 import QtGui
from PyQt5 import QtCore


class Painter(QtGui.QPainter):

    def __init__(self, q_widget):
        super().__init__(q_widget)

    def __enter__(self):
        self.begin(self.device())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end()
        return isinstance(exc_val, TypeError)


class Item:

    def update(self):
        pass

    def draw(self, painter):
        pass


class Mower(Item):

    def __init__(self):
        self.x = 0
        self.y = 0

    def update(self):
        self.x += 2
        self.y += 1

    def draw(self, painter):
        painter.fillRect(self.x, self.y, 20, 20, QtGui.QBrush(QtGui.QColor(0, 200, 0), QtCore.Qt.SolidPattern))

