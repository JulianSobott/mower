"""
@author: Julian
@brief:
@description:
"""
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import QRect

from .Logging import logger
import Core
from .Painting import Renderable
from utils import Length


class Mower(Core.Mower, Renderable):

    def __init__(self):
        self.x = Length(1, Length.METER)
        self.y = Length(1, Length.METER)
        self.rotation = 0   # like compass (0 - 360)

    def rotate_wheel(self, wheel, deg):
        # TODO: implement
        pass

    def get_sensor_data(self):
        # TODO: implement
        pass

    def update(self):
        super().update()
        self.rotation += 10
        self.x += Length(1, Length.PIXEL)
        self.y += Length(1, Length.PIXEL)

    def draw(self, painter):
        """
        The center of the mower is the x and y coordinates
        The mower is rotated around the center
        """
        rect = QRect(self.x.pixel(), self.y.pixel(), self.WIDTH.pixel(), self.LENGTH.pixel())

        transform = QtGui.QTransform()
        center_point = rect.center()

        # Sets the center as 0;0 coordinate
        transform.translate((-self.WIDTH/2).pixel(), (-self.LENGTH/2).pixel())

        # Rotate around the center
        transform.translate(center_point.x(), center_point.y())
        transform.rotate(self.rotation)
        transform.translate(-center_point.x(), -center_point.y())

        painter.setTransform(transform)

        painter.fillRect(rect, QtGui.QBrush(QtGui.QColor(0, 200, 0), QtCore.Qt.SolidPattern))

        painter.resetTransform()
