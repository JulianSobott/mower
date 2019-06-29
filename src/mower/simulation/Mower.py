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
from mower.simulation import paths


class Mower(core.Mower, Renderable):
    MOWER_COLOR = QtGui.QColor(150, 120, 150)

    def __init__(self):
        super().__init__()
        #: The position on the global map
        #: The global map must always be updated synchronously to the local position
        self.global_pos: types.PointL = [Length(1, Length.METER), Length(1, Length.METER)]

        #: Map where all the sensor data is taken from
        self.global_map: simulation.Map = None

        self.img_mower = QtGui.QImage(paths.get_asset_path("mower.png"))

    def update_rendering(self, passed_time: float):
        """Periodically updating the state of the mower."""
        super().update(passed_time)

    def draw(self, painter):
        """
        The center of the mower is the x and y coordinates
        The mower is rotated around the center
        """

        rect = QRect(self.global_pos[0].pixel(), self.global_pos[1].pixel(), self.WIDTH.pixel(), self.LENGTH.pixel())

        transform = QtGui.QTransform()
        center_point = rect.center()

        # Sets the center as 0;0 coordinate
        transform.translate((-self.WIDTH / 2).pixel(), (-self.LENGTH / 2).pixel())

        # Rotate around the center
        transform.translate(center_point.x(), center_point.y())
        transform.rotate(self.look_direction_deg)
        transform.translate(-center_point.x(), -center_point.y())

        painter.setTransform(transform, combine=True)

        # painter.fillRect(rect, QtGui.QBrush(self.MOWER_COLOR, QtCore.Qt.SolidPattern))
        painter.drawImage(rect, self.img_mower)

        painter.resetTransform()

    def rotate_wheel(self, wheel, deg):
        pass

    def rotate_wheels(self, time_left, time_right):
        pass

    def drive_forward(self, distance: Length):
        d_x, d_y = super().drive_forward(distance)

        self.global_pos[0] += d_x
        self.global_pos[1] += d_y

    def get_sensor_data(self):
        underground = self.global_map.cell_type_at(*self.global_pos)
        return core.SensorData(underground)

    def _load_map(self) -> 'simulation.Map':
        return simulation.Map()

    def update_map(self, data):
        super().update_map(data)

        # row_start, col_start = self.local_map.pos2index(*self.last_local_pos)
        # row_end, col_end = self.local_map.pos2index(*self.local_pos)
        # self.local_map.add_line_data((col_start, row_start), (col_end, row_end), self.WIDTH.pixel(),
        #                              self.global_map.cells, 1)
