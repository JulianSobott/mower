"""
@author: Julian
@brief:
@description:
    width
    _____
   |  ^  |
   |     |   length
   |     |
    -----
"""
from typing import Tuple

import math

from mower.core.Logging import logger
from mower.utils import Length
from mower import core
from mower.utils import types


class Mower:
    """Abstract class"""

    LEFT_WHEEL = 0
    RIGHT_WHEEL = 1

    VELOCITY_MS = 0.001  # m/s

    WIDTH = Length(0.3, Length.METER)
    LENGTH = Length(0.5, Length.METER)
    HEIGHT = Length(0.3, Length.METER)

    WHEEL_RADIUS = Length(7, Length.CENTIMETER)
    WHEEL_DISTANCE = WIDTH  # distance from 1 wheel to the other. measured from both centers

    def __init__(self):
        #: Map that contains all data that the mower is aware of
        self.local_map: core.Map = self._load_map()

        #: Position of the mower on the local map
        #: Mower should start somewhere in the middle to have enough space to build the map around itself
        #: Indices: 0 = X = Horizontal = Col, 1 = Y = Vertical = Row
        self.local_pos: types.PointL = [Length(1, Length.METER), Length(1, Length.METER)]

        #: Position of the last call circle
        self.last_local_pos: types.PointL = self.local_pos.copy()
        logger.debug(f"{id(self.local_pos)}, {id(self.last_local_pos)}")

        #: The direction, the front of the mower faces. The int is a compass number
        #: E.g. North = 0, East = 90, South = 180, West = 270
        #: Value Range inclusive: 0 - 359
        self.look_direction_deg: int = 150
        self.look_direction_rad: float = math.radians(self.look_direction_deg)

    def drive(self):
        distance_to_drive = 0
        deg_to_turn = 0
        is_on = True
        while is_on:
            # calculate way

            if distance_to_drive > 0:
                pass
                # keep moving
            else:
                pass
                # stop wheels

            if deg_to_turn > 0:
                pass
                # keep turning
            else:
                pass
                # stop wheels

    def rotate_wheels(self, time_left, time_right):
        """Implement this function in child class
        WHEEL can be self.LEFT_WHEEL or self.RIGHT_WHEEL"""
        raise NotImplementedError

    def get_sensor_data(self) -> 'SensorData':
        """Implement this function in child class"""
        raise NotImplementedError

    def update(self, delta_time: float):
        """Takes all data calculates next actions and execute them
        Way algorithm could go here?"""
        data = self.get_sensor_data()
        self.update_map(data)
        distance = Length(self.VELOCITY_MS * delta_time, Length.METER)
        self.last_local_pos = self.local_pos.copy()
        self.drive_forward(distance)

    def update_map(self, data: 'SensorData'):
        #self.local_map.add_line_data((10, 10), (200, 200), 10, self.local_map.cells, 2)
        # self.local_map.add_line_data((200, 0), (0, 200), 4, self.local_map.cells, 2)
        # logger.debug(id(self.local_map.cells))
        # logger.debug(f"{self.last_local_pos}, {self.local_pos}")
        row_start, col_start = self.local_map.pos2index(*self.last_local_pos)
        row_end, col_end = self.local_map.pos2index(*self.local_pos)
        self.local_map.add_line_data((col_start, row_start), (col_end, row_end), self.WIDTH.pixel(),
                                     self.local_map.cells, data.cell_type.value)

    def drive_forward(self, distance: Length) -> types.PointL:
        """

        :param distance:
        :return: [d_x, d_y] The distances that where driven in X and Y direction
        """
        # TODO self.rotate_wheels()
        d_y = math.sin(self.look_direction_rad - math.pi/2) * distance
        d_x = math.cos(self.look_direction_rad - math.pi/2) * distance
        self.local_pos[0] += d_x
        self.local_pos[1] += d_y
        return [d_x, d_y]

    def drive_forward_till_obstacle(self):
        # Necessary?
        pass

    def turn(self, deg):
        pass
        # TODO: implement
        # Calls rotate_wheel()

    def _load_map(self) -> 'core.Map':
        """If a map is saved load it else create a new one."""
        return core.Map()


class SensorData:

    def __init__(self, underground: 'core.CellType'):
        self.cell_type = underground

    def __repr__(self):
        return f"SensorData(underground = {self.cell_type},)"
