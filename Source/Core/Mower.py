"""
@author: Julian
@brief:
@description:
"""

from .Logging import logger


class Mower:
    """Abstract class"""

    LEFT_WHEEL = 0
    RIGHT_WHEEL = 1

    def __init__(self):
        pass

    def rotate_wheel(self, wheel, deg):
        """Implement this function in child class"""
        pass

    def get_sensor_data(self):
        """Implement this function in child class"""
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
