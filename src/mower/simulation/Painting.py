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
from PyQt5 import QtWidgets

from mower.simulation.Logging import logger


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

    def update_rendering(self, passed_time):
        logger.error("implement this function in child class: update_rendering")
        pass

    def draw(self, painter: Painter, *args):
        logger.error("implement this function in child class: draw")
        pass

