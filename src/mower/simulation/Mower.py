"""
@author: Julian
@brief:
@description:
"""
from typing import Tuple

import math

from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import QRect

from mower.simulation.Logging import logger
from mower.simulation.Painting import Renderable
from mower.utils import types, Length
from mower import core, simulation
from mower.simulation import paths, Painting


class Mower(core.Mower, Renderable):

    MOWER_COLOR = QtGui.QColor(150, 120, 150)

    def __init__(self):
        super().__init__()

        #: The position on the global map
        #: The global map must always be updated synchronously to the local position
        self.global_pos: types.PointL = [Length(3, Length.METER), Length(3, Length.METER)]

        #: Map where all the sensor data is taken from
        self.global_map: simulation.Map = None

        self.img_mower = QtGui.QImage(paths.get_asset_path("mower.png"))

    def update_rendering(self, passed_time: float):
        """Periodically updating the state of the mower. """

        super().update(passed_time)

    def draw(self, painter: Painting.Painter, is_global: bool = False) -> None:
        """
        The center of the mower is the x and y coordinates
        The mower is rotated around the center

        :param painter:
        :param is_global: Defines if the global or the local position is taken for rendering
        """
        if is_global:
            rect = QRect(self.global_pos[0].pixel(), self.global_pos[1].pixel(), self.WIDTH.pixel(), self.LENGTH.pixel())
        else:
            rect = QRect(self.local_pos[0].pixel(), self.local_pos[1].pixel(), self.WIDTH.pixel(), self.LENGTH.pixel())

        r_x = self.global_pos[0] - self.WIDTH
        r_y = self.global_pos[1] - self.LENGTH / 2

        world_rx = r_x * math.cos(self.look_direction_rad) - math.sin(self.look_direction_rad) * r_y
        world_ry = r_x * math.sin(self.look_direction_rad) + math.cos(self.look_direction_rad) * r_y

        #logger.debug(f"{world_rx }, {world_ry}")

        transform = QtGui.QTransform()
        center_point = rect.center()

        # Sets the center as 0;0 coordinate
        transform.translate((-self.WIDTH / 2).pixel(), (-self.LENGTH).pixel())

        # Rotate around the center
        transform.translate(center_point.x(), center_point.y())
        transform.rotate(self.look_direction_deg)
        transform.translate(-center_point.x(), -center_point.y())

        painter.setTransform(transform, combine=True)

        painter.fillRect(rect, QtGui.QBrush(self.MOWER_COLOR, QtCore.Qt.SolidPattern))
        painter.drawImage(rect, self.img_mower)

        painter.resetTransform()

    def get_sensor_data(self):
        return

    def _update_position(self, delta_time: float) -> types.PointL:
        dx, dy = super()._update_position(delta_time)
        self.global_pos[0] += dx
        self.global_pos[1] += dy
        return [dx, dy]

    def _load_map(self) -> 'simulation.Map':
        return simulation.Map()

    def _output_motors_data(self) -> None:
        pass

    def reset(self):
        self.__init__()
