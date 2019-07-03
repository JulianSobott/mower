"""
:module: mower.core.map_utils
:synopsis: Classes and functions for the map
:author: Julian Sobott
:author: 

public functions
-----------------

.. autofunction:: XXX

public classes
-----------------

.. autoclass:: XXX
    :members:


private functions
------------------

.. autofunction:: XXX

private classes
-----------------

.. autoclass:: XXX
    :members:

"""
from typing import Union, Type

import numpy as np

from mower.utils import types


class Quad:

    SURROUND_WITH_BORDER = True     # just for debugging

    def __init__(self, init_value, shape, data_type: Type = np.uint8, parent: 'Quad' = None):
        self.parent: Quad = parent

        #: rows, cols or Height, Width
        self.shape = shape

        if self.SURROUND_WITH_BORDER and data_type == np.uint8:
            self.data = np.full(shape, 0, dtype=data_type)
            border_width = 3
            self.data[border_width:-border_width, border_width:-border_width] = init_value
        else:
            #: can contain either an array with other quads or primitive data
            self.data = np.full(shape, init_value, dtype=data_type)

        #: True: data contains primitives, False: data contains Quads
        # TODO
        self.is_leaf = True

    def value_at(self, x: int, y: int) -> Union[int, 'Quad']:
        """

        :param x:
        :param y:
        :return:
        """
        return self.data[y][x]

    def grow(self, amount: int, direction: types.Direction, init_value) -> None:
        """
        Increases the size of the data array and fills the new fields with `init_value`.
        :param amount: Amount of rows/columns are added
        :param direction: In which direction are the fields added
        :param init_value:
        :return:
        """
        axis_direction = {types.NORTH: 0, types.EAST: 1, types.SOUTH: 0, types.WEST: 1}
        if axis_direction[direction] == 0:
            self.shape = (self.shape[0] + amount, self.shape[1])
            appendix = np.full((amount, self.shape[1]), init_value)
        else:
            self.shape = (self.shape[0], self.shape[1] + amount)
            appendix = np.full((self.shape[0], amount), init_value)

        if direction == types.NORTH or direction == types.WEST:
            a = appendix
            b = self.data
        else:
            a = self.data
            b = appendix
        self.data = np.concatenate((a, b), axis=axis_direction[direction])

    def fill_with_quads(self, init_value, shape, data_type: Type = np.uint8):
        for row in range(self.shape[0]):
            for col in range(self.shape[1]):
                if self.data[row][col] is None:
                    self.data[row][col] = Quad(init_value, shape, data_type, self)

    def __getitem__(self, item) -> np.ndarray:
        return self.data[item]

    def __setitem__(self, key, value):
        self.data[key] = value



if __name__ == '__main__':
    qt = Quad(0, (2, 2), int)
    print(qt.data)
    qt.grow(4, types.NORTH, 1)
    print(qt.data)
    qt.grow(2, types.EAST, 2)
    print(qt.data)
    q = Quad(None, (2, 2), Quad)
    q.grow(2, types.NORTH, Quad(1, (2, 2), int, q))
    print(q.data)