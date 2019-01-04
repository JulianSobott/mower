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

from .Logging import logger


class Painter(QtGui.QPainter):

    def __init__(self, q_widget):
        super().__init__(q_widget)

    def __enter__(self):
        self.begin(self.device())
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end()
        return isinstance(exc_val, TypeError)


class Renderable:

    def update(self):
        logger.error("implement this function in child class: rotate_wheel")
        pass

    def draw(self, painter):
        logger.error("implement this function in child class: rotate_wheel")
        pass

