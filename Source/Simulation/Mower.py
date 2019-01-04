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
from utils import Converter


class Mower(Core.Mower, Renderable):
    # in 2d space for drawing
    WIDTH = Converter.metres_2_px(0.3)
    HEIGHT = Converter.metres_2_px(0.5)

    def __init__(self):
        self.x = Converter.metres_2_px(0.3)
        self.y = Converter.metres_2_px(0)
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
        self.x += 1
        self.y += 1

    def draw(self, painter):
        """
        The center of the mower is the x and y coordinates
        The mower is rotated around the center
        """
        rect = QRect(self.x, self.y, self.WIDTH, self.HEIGHT)

        transform = QtGui.QTransform()
        center_point = rect.center()

        # Sets the center as 0;0 coordinate
        transform.translate(-self.WIDTH/2, -self.HEIGHT/2)

        # Rotate around the center
        transform.translate(center_point.x(), center_point.y())
        transform.rotate(self.rotation)
        transform.translate(-center_point.x(), -center_point.y())

        painter.setTransform(transform)
        painter.fillRect(rect, QtGui.QBrush(QtGui.QColor(0, 200, 0), QtCore.Qt.SolidPattern))

        painter.resetTransform()
