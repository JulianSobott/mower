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
from mower.core.map_utils import Quad, DATA_SHAPE
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
    """
    The map stores data for each cell. It is build up from :class:`mower.core.map_utils.Quad` 's.
    """
    #: How big is a cell in the real world. The smaller the value the more precise is the map, but also the bigger it
    #: gets (memory).
    #: Use the converter unit to fit pixel conversion properly
    CELL_SIZE = Length(1/Converter.PX2M_DIVIDER, Length.METER)

    def __init__(self):
        self.root_quad = Quad(None, (2, 2), Quad)
        self.root_quad.fill_with_quads(CellType.GRASS.value, DATA_SHAPE)

    def add_line_data(self, pos1: Point, pos2: Point, thickness: int, data_val: int):
        # TODO: find way that ensures, that line is always thick enough (take angular in account)
        poly = np.array((
            (pos1[1] + thickness // 2, pos1[0] + thickness // 2),   # top left
            (pos1[1] - thickness // 2, pos1[0] - thickness // 2),   # bottom left
            (pos2[1] - thickness // 2, pos2[0] - thickness // 2),   # bottom right
            (pos2[1] + thickness // 2, pos2[0] + thickness // 2),   # top right
        ))
        poly += (np.array(self.root_quad.offset) * np.array(DATA_SHAPE))[[1, 0]]
        rr, cc = skimage.draw.polygon(poly[:, 0], poly[:, 1])
        rr -= self.root_quad.offset[1] * DATA_SHAPE[1]
        cc -= self.root_quad.offset[0] * DATA_SHAPE[0]

        self.root_quad.set_data_by_indices(rr, cc, data_val)
