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

from .Logging import logger
from utils import Length


class Mower:
    """Abstract class"""

    LEFT_WHEEL = 0
    RIGHT_WHEEL = 1

    WIDTH = Length(0.3, Length.METER)
    LENGTH = Length(0.5, Length.METER)
    HEIGHT = Length(0.3, Length.METER)

    def __init__(self):
        pass

    def rotate_wheel(self, wheel, deg):
        """Implement this function in child class"""
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

    def turn(self, deg):
        pass
        # TODO: implement
        # Calls rotate_wheel()

