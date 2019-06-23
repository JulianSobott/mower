"""
@author: Julian
@brief:
@description:
"""
import math

from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import QRect

from mower.simulation.Logging import logger
from mower.simulation.Painting import Renderable
from mower.utils import Length
from mower import core, simulation
from mower.simulation import paths


class Mower(core.Mower, Renderable):

    MOWER_COLOR = QtGui.QColor(150, 120, 150)

    def __init__(self):
        super().__init__()
        self.x = Length(2, Length.METER)
        self.y = Length(3, Length.METER)
        self.rotation = 90   # like compass (0 - 360)
        self.local_map: simulation.Map

        self.img_mower = QtGui.QImage(paths.get_asset_path("mower.png"))

    def rotate_wheel(self, wheel, deg):
        distance = 2 * math.pi * self.WHEEL_RADIUS * deg/360
        distance = math.pi * self.WIDTH / 2
        # with non rotated coord. system
        alpha = math.atan((distance/self.WHEEL_DISTANCE).pixel())
        alpha_deg = math.degrees(alpha)
        delta_y = math.sin(alpha) * (self.WIDTH / 2)
        adjacent = Length(math.sqrt((((self.WIDTH / 2) ** 2) - (delta_y ** 2)).pixel()), Length.PIXEL)
        delta_x = adjacent - self.WIDTH

        # with rotated coord. system
        """
        hypotenuse = Length(math.sqrt((delta_x**2 + delta_y**2).pixel()), Length.PIXEL)
        full_rotation_degree = self.rotation + alpha_deg
        real_delta_y = Length(math.asin(full_rotation_degree) * hypotenuse, Length.PIXEL)
        real_delta_x = Length(math.acos(full_rotation_degree) * hypotenuse, Length.PIXEL)
        """

        self.y += delta_y
        self.x += delta_x

        if wheel == self.LEFT_WHEEL:
            self.rotation += alpha_deg
        else:
            self.rotation -= alpha_deg

        pass

    def get_sensor_data(self):
        # TODO: implement
        pass

    def update_rendering(self, passed_time):
        super().update()
        # TODO:
        #self.rotate_wheel(self.RIGHT_WHEEL, 1)

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

        painter.setTransform(transform, True)

        # painter.fillRect(rect, QtGui.QBrush(self.MOWER_COLOR, QtCore.Qt.SolidPattern))
        painter.drawImage(rect, self.img_mower)

        painter.resetTransform()

    def _load_map(self) -> 'simulation.Map':
        return simulation.Map()
