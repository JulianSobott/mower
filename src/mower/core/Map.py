"""
:module: mower.core.Map
:synopsis: A map can store the data of all cells
:author: Julian Sobott
:author:

public classes
----------------------

.. autoclass:: Map
    :members:

"""
from typing import Union

import numpy as np

import skimage.draw

from mower.core import CellType
from mower.core.map_utils import Quad, DATA_SHAPE
from mower.utils import Length
from mower.utils.types import Point
from mower.utils import Converter
from mower.core.Logging import logger


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
        self.reset()

        #: After which time (in seconds) every grass cell 'grows'
        self._grass_update_time = 0.5
        #: Time passed since the last grow
        self._passed_last_grown = 0

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

    def update(self, passed_time: Union[float, int]):
        self._passed_last_grown += passed_time
        if self._passed_last_grown >= self._grass_update_time:
            self.root_quad.grow_grass_cells()
            self._passed_last_grown = 0

    def get_value_at(self, x: int, y: int) -> int:
        """

        :param x: position
        :param y: position
        :return: CellType value
        """
        return self.root_quad.get_value_at(x, y)

    def set_value_at(self, x: int, y: int, value: int) -> None:
        """

        :param x: position
        :param y: position
        :param value: CellType value
        :return: None
        """
        return self.root_quad.set_value_at(x, y, value)

    def get_array_at(self, x: int, y: int, width: int, height: int) -> np.ndarray:
        """

        :param x: position
        :param y: position
        :param width:
        :param height:
        :return: An Array filled with the data of a rectangle area with geometry: x, y, width, height
        """
        return self.root_quad.get_array_at(x, y, width, height)

    def set_data_by_array(self, array: np.ndarray, x: int, y: int):
        """

        :param array: numpy integer array filled with the new data
        :param x: position on the map. Can be negative
        :param y: position on the map. Can be negative
        :return:
        """
        return self.root_quad.set_data_by_array(array, x, y)

    def get_data_by_positions(self, y_values: np.ndarray, x_values: np.ndarray) -> np.ndarray:
        """

        :param y_values: numpy array of y positions
        :param x_values: numpy array of x positions (matching thr y positions)
        :return: numpy array with all data
        """
        return self.root_quad.get_data_by_positions(y_values, x_values)

    def reset(self):
        """

        :return:
        """
        self.root_quad = Quad(None, (2, 2), Quad)
        self.root_quad.fill_with_quads(CellType.GRASS.value, DATA_SHAPE)
