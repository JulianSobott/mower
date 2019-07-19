"""
:module: mower.simulation.Mower
:synopsis: Core class to control the Mower
:author: Julian Sobott
:author:

::

    width
    _____
   |  ^  |
   |     |   length
   |     |
    -----
    
public classes
-----------------

.. autoclass:: Mower
    :members:
    :undoc-members:
    :private-members:
    
.. autoclass:: SensorData
    :members:
    :undoc-members:

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

        #: Output signal for left motor
        self.left_motor_speed: int = 0
        self.left_motor_direction: types.MotorDirection = types.MOTOR_DIRECTION_FORWARD

        #: Output signal for right motor
        self.right_motor_speed: int = 0
        self.right_motor_direction: types.MotorDirection = types.MOTOR_DIRECTION_FORWARD

    def stop_motors(self) -> None:
        """
        Stops both motors

        :return:
        """
        self.set_motors(0, types.MOTOR_DIRECTION_FORWARD, 0, types.MOTOR_DIRECTION_FORWARD)

    def forward(self, speed: int) -> None:
        """
        Sets both motors to run forwards at speed.

        :param speed: TODO: Description of speed needed
        """
        self.set_motors(speed, types.MOTOR_DIRECTION_FORWARD, speed, types.MOTOR_DIRECTION_FORWARD)

    def reverse(self, speed: int) -> None:
        """
        Sets both motors to run in reverse at speed.

        :param speed: TODO: Description of speed needed
        """
        self.set_motors(speed, types.MOTOR_DIRECTION_BACKWARD, speed, types.MOTOR_DIRECTION_BACKWARD)

    def turn_forwards(self, left_speed: int, right_speed: int) -> None:
        """
        Moves forward in an arc by setting different speeds.

        :param left_speed:
        :param right_speed:
        """
        self.set_motors(left_speed, types.MOTOR_DIRECTION_FORWARD, right_speed, types.MOTOR_DIRECTION_FORWARD)

    def turn_backwards(self, left_speed: int, right_speed: int) -> None:
        """
        Moves forward in an arc by setting different speeds.

        :param left_speed:
        :param right_speed:
        """
        self.set_motors(left_speed, types.MOTOR_DIRECTION_BACKWARD, right_speed, types.MOTOR_DIRECTION_BACKWARD)

    def set_motors(self, left_speed: int, left_direction: types.MotorDirection,
                   right_speed: int, right_direction: types.MotorDirection):
        """
        Full Control over both motors. All other movement functions call this function.

        :param left_speed:
        :param left_direction:
        :param right_speed:
        :param right_direction:
        :return:
        """
        self.left_motor_speed = left_speed
        self.left_motor_direction = left_direction
        self.right_motor_speed = right_speed
        self.right_motor_direction = right_direction

    def _drive(self) -> None:
        """
        Drives based on the :attr:`left_motor_speed`, :attr:`left_motor_direction`,
        :attr:`right_motor_speed`, :attr:`right_motor_direction`,

        :return:
        """
        raise NotImplementedError

    def get_sensor_data(self) -> 'SensorData':
        """
        Collects all data from all sensors.

        :return: A :class:`SensorData` object, that stores all data.
        """
        raise NotImplementedError

    def update(self, delta_time: float):
        """Takes all data calculates next actions and execute them.
        Way algorithm could go here?"""
        data = self.get_sensor_data()
        self.update_map(data)

    def update_map(self, data: 'SensorData'):
        pass

    def _load_map(self) -> 'core.Map':
        """If a map is saved load it else create a new one."""
        return core.Map()


class SensorData:

    def __init__(self, front_underground):
        #: Underground data, that is directly in front of the mower
        self.front_underground = front_underground

    def __repr__(self):
        return f"SensorData(front_underground = {self.front_underground},)"

