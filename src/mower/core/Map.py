"""
:module: mower.core.Map
:synopsis: A map can store the data of all cells
:author: Julian Sobott
:author:

public classes
----------------------

.. autoclass:: Map
    :members:

.. autoclass:: CellType
    :members:


"""
from typing import Tuple

import numpy as np
import enum

import skimage.draw

from mower.core.Logging import logger
from mower.utils import Length
from mower.utils.types import Point
from mower.utils import Converter


class CellType(enum.Enum):

    UNDEFINED = 0
    GRASS = 1
    OBSTACLE = 2

    @classmethod
    def by_value(cls, val):
        return {0: cls.UNDEFINED, 1: cls.GRASS, 2: cls.OBSTACLE}[val]


class Map:

    #: How big is a cell in the real world. The smaller the value the more precise is the map, but also the bigger it
    #: gets (memory).
    #: Use the converter unit to fit pixel conversion properly
    CELL_SIZE = Length(1/Converter.PX2M_DIVIDER, Length.METER)

    def __init__(self, size: Tuple[Length, Length] = (Length(50, Length.METER), Length(50, Length.METER))):

        #: The actual size in the real world
        self.size = size

        #: The array shape, based on CELL_SIZE
        self.shape = int((self.size[0] / self.CELL_SIZE).length), int((self.size[1] / self.CELL_SIZE).length)

        #: The cell type for every cell
        self.cells = np.zeros(self.shape)

    def __getitem__(self, index):
        return self.cells[index]

    @staticmethod
    def add_line_data(pos1: Point, pos2: Point, thickness: int, data: np.array, data_val: int):
        # TODO: find way that ensures, that line is always thick enough (take angular in account)
        poly = np.array((
            (pos1[1] + thickness // 2, pos1[0] + thickness // 2),
            (pos2[1] + thickness // 2, pos2[0] + thickness // 2),
            (pos2[1] - thickness // 2, pos2[0] - thickness // 2),
            (pos1[1] - thickness // 2, pos1[0] - thickness // 2),
        ))
        rr, cc = skimage.draw.polygon(poly[:, 0], poly[:, 1])
        data[rr, cc] = data_val

    def pos2index(self, x: Length, y: Length) -> Tuple[int, int]:
        """Transfer the position of the mower on the map to [row, col] indices of the map array."""
        return (y / self.CELL_SIZE).int_val(), (x / self.CELL_SIZE).int_val()

    def index2pos(self, row: int, col: int):
        return col * self.CELL_SIZE, row * self.CELL_SIZE
