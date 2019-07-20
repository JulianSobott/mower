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

Driving procedure:
----------------------

This procedure is executed periodically multiple times per seconds in :meth:`Mower.update()`.

1. Get Sensor data
2. Update map, based on sensor data
3. Calculate next step(s)
4. Set parameters of the motors
5. Output the motor parameters
    
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

        #: Output signal for left motor. Range: 0 <= speed <= 100
        self.left_motor_speed: int = 0
        self.left_motor_direction: types.Direction_2D = types.DIRECTION_FORWARD

        #: Output signal for right motor. Range: 0 <= speed <= 100
        self.right_motor_speed: int = 0
        self.right_motor_direction: types.Direction_2D = types.DIRECTION_FORWARD

    def stop_motors(self) -> None:
        """
        Stops both motors

        :return:
        """
        self.set_motors(0, types.DIRECTION_FORWARD, 0, types.DIRECTION_FORWARD)

    def forward(self, speed: int = 100) -> None:
        """
        Drive forward with speed.

        :param speed: 0: stop <= speed <= 100: max speed
        """
        self.set_motors(speed, types.DIRECTION_FORWARD, speed, types.DIRECTION_FORWARD)

    def backward(self, speed: int = 100) -> None:
        """
        Drive backward with speed.

        :param speed: 0: stop <= speed <= 100: max speed
        """
        self.set_motors(speed, types.DIRECTION_BACKWARD, speed, types.DIRECTION_BACKWARD)

    def turn_around_center(self, deg: int, clockwise: bool = True) -> None:
        """
        Turns the given amount. The position of the center stays the same.

        :param deg: Angular to turn in degree. 0 < deg < 360
        :param clockwise: In which direction to to turn
        """
        assert 0 < deg < 360, f"Value is not in range: 0 < {deg} < 360"
        raise NotImplementedError   # TODO

    def turn_around_wheel(self, deg: int, wheel: types.Side, clockwise: bool = True):
        """
        Turns the given amount around the given wheel. So the position of the passed wheel stays the same.

        :param deg: Angular to turn in degree. 0 < deg < 360
        :param wheel: Wheel that is fixed
        :param clockwise: In which direction to to turn
        :return:
        """
        assert 0 < deg < 360, f"Value is not in range: 0 < {deg} < 360"
        raise NotImplementedError  # TODO

    def drive_arc(self, radius: Length, direction: types.Direction_2D, side: types.Side):
        """
        Drives an arc in the given radius.

        :param radius: Radius measured from the center of the mower.
        :param direction: Drive forward or backward
        :param side: Drive to the left or to the right
        :return:
        """

    def set_motors(self, left_speed: int, left_direction: types.Direction_2D,
                   right_speed: int, right_direction: types.Direction_2D):
        """
        Full Control over both motors. All other movement functions call this function.

        :param left_speed:
        :param left_direction:
        :param right_speed:
        :param right_direction:
        :return:
        """
        assert 0 <= left_speed <= 100, "Left speed value must be in range: 0 <= speed <= 100"
        assert 0 <= right_speed <= 100, "Right speed value must be in range: 0 <= speed <= 100"
        self.left_motor_speed = left_speed
        self.left_motor_direction = left_direction
        self.right_motor_speed = right_speed
        self.right_motor_direction = right_direction

    def _output_motors_data(self) -> None:
        """
        Outputs all motor parameters to the motors: :attr:`left_motor_speed`, :attr:`left_motor_direction`,
        :attr:`right_motor_speed`, :attr:`right_motor_direction`. Only needed in :mod:`mower.real`.
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

    def _update_position(self, delta_time: float) -> None:
        """Update the position based on the delta time and the motors parameters.

        :param delta_time: Time passed since last update.
        """

    def _load_map(self) -> 'core.Map':
        """If a map is saved load it else create a new one."""
        return core.Map()


class SensorData:

    def __init__(self, front_underground):
        #: Underground data, that is directly in front of the mower
        self.front_underground = front_underground

    def __repr__(self):
        return f"SensorData(front_underground = {self.front_underground},)"

