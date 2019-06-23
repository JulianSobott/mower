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

from mower.core.Logging import logger
from mower.utils import Length
from mower import core


class Mower:
    """Abstract class"""

    LEFT_WHEEL = 0
    RIGHT_WHEEL = 1

    VELOCITY_MS = 0.1  # m/s

    WIDTH = Length(0.3, Length.METER)
    LENGTH = Length(0.5, Length.METER)
    HEIGHT = Length(0.3, Length.METER)

    WHEEL_RADIUS = Length(7, Length.CENTIMETER)
    WHEEL_DISTANCE = WIDTH  # distance from 1 wheel to the other. measured from both centers

    def __init__(self):
        #: Map that contains all data that the mower is aware of
        self.local_map: core.Map = self._load_map()

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
        logger.error("implement this function in child class")
        pass

    def get_sensor_data(self):
        """Implement this function in child class"""
        logger.error("implement this function in child class: rotate_wheel")
        pass

    def update(self):
        """Takes all data calculates next actions and execute them
        Way algorithm could go here?"""
        # TODO: implement
        pass

    def drive_forward(self, distance):
        pass

        # TODO: implement
        # Calls rotate_wheel()

    def drive_forward_till_obstacle(self):
        # Necessary?
        pass

    def turn(self, deg):
        pass
        # TODO: implement
        # Calls rotate_wheel()

    def _load_map(self) -> core.Map:
        """If a map is saved load it else create a new one."""
        return core.Map()
