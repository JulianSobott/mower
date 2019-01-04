"""
@author: Julian
@brief:
@description:
"""
from PyQt5 import QtGui
from PyQt5 import QtCore

from .Logging import logger
import Core
from .Painting import Renderable


class Mower(Core.Mower, Renderable):

    def __init__(self):
        self.x = 0
        self.y = 0

    def rotate_wheel(self, wheel, deg):
        # TODO: implement
        pass

    def get_sensor_data(self):
        # TODO: implement
        pass

    def update(self):
        self.x += 2
        self.y += 1

    def draw(self, painter):
        painter.fillRect(self.x, self.y, 20, 20, QtGui.QBrush(QtGui.QColor(0, 200, 0), QtCore.Qt.SolidPattern))
