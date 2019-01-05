"""
@author: Julian
@brief:
@description:

Expandable array in all directions
Different sizes
"""

from .Logging import logger
from utils import Length


class Cell:

    SIZE = Length(5, Length.CENTIMETER)

    def __init__(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y
        self.neighbors = []

class GrasslandCell(Cell):

    IS_PASSABLE = True
    pass


class ObstacleCell(Cell):

    IS_PASSABLE = False
    pass


class Map:

    def __init__(self):
        self.cells = []

    def update(self):
        pass
