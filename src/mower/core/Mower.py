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

    #: Constants
    LEFT_WHEEL = 0
    RIGHT_WHEEL = 1

    #: m/s
    VELOCITY_MS = 0.5

    WIDTH = Length(0.3, Length.METER)
    LENGTH = Length(0.5, Length.METER)
    HEIGHT = Length(0.3, Length.METER)

    WHEEL_RADIUS = Length(7, Length.CENTIMETER)

    #: Distance from one wheel to the other. Measured from both centers
    WHEEL_DISTANCE = WIDTH

    def __init__(self):
        #: Map that contains all data that the mower is aware of
        self.local_map: core.Map = self._load_map()

        #: Position of the mower on the local map
        #: Mower should start somewhere in the middle to have enough space to build the map around itself
        #: Indices: 0 = X = Horizontal = Col, 1 = Y = Vertical = Row
        self.local_pos: types.PointL = [Length(1, Length.METER), Length(1, Length.METER)]

        #: Position of the last call circle
        self.last_local_pos: types.PointL = self.local_pos.copy()

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
        """Takes all data calculates next actions and execute them.
        Way algorithm could go here?"""
        # data = self.get_sensor_data()
        # self.update_map(data)
        distance = Length(self.VELOCITY_MS * delta_time, Length.METER)
        self.last_local_pos = self.local_pos.copy()
        self.drive_forward(distance)

    def update_map(self, data: 'SensorData'):
        pass

    def drive_forward(self, distance: Length) -> types.PointL:
        """

        :param distance:
        :return: [d_x, d_y] The distances that were driven in X and Y direction
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

    def __init__(self, front_underground):
        #: Underground data, that is directly in front of the mower
        self.front_underground = front_underground

    def __repr__(self):
        return f"SensorData(front_underground = {self.front_underground},)"
