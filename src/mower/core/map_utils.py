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
from mower.core.Logging import logger

DEFAULT_DATA_SHAPE = (500, 500)


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

        #: How many quads added to the LEFT and to the TOP
        self.offset = [0, 0]
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

    def grow(self, amount: int, direction: types.Direction, init_value, shape=None, create_quads=False) -> None:
        """
        Increases the size of the data array and fills the new fields with `init_value`.
        :param amount: Amount of rows/columns are added
        :param direction: In which direction are the fields added
        :param init_value:
        :param shape:
        :param create_quads:
        :return:
        """
        if amount <= 0:
            return
        logger.debug(f"Grow: {amount} in {direction}")
        axis_direction = {types.NORTH: 0, types.EAST: 1, types.SOUTH: 0, types.WEST: 1}
        if direction == types.NORTH:
            self.offset[1] += amount
        elif direction == types.WEST:
            self.offset[0] += amount

        if axis_direction[direction] == 0:
            self.shape = (self.shape[0] + amount, self.shape[1])
            if create_quads:
                appendix = np.array([[Quad(init_value, shape, parent=self) for _ in range(self.shape[1])]
                                     for __ in range(amount)])
            else:
                appendix = np.full((amount, self.shape[1]), init_value)
        else:
            self.shape = (self.shape[0], self.shape[1] + amount)
            if create_quads:
                appendix = np.array([[Quad(init_value, shape, parent=self) for _ in range(amount)]
                                     for __ in range(self.shape[0])])
            else:
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

    def grow_to_size(self, target_geometry):
        """

        :param target_geometry: x, y, width, height
        :return:
        """
        quad_shape = self.data[0][0].shape
        pos_x = -(self.offset[0] * quad_shape[1])
        pos_y = -(self.offset[1] * quad_shape[0])
        # grow to the left
        if target_geometry[0] < pos_x:
            left_space = abs(target_geometry[0] - pos_x)
            if left_space > 0:
                extra_quads = np.math.ceil(left_space / quad_shape[1])
                self.grow(extra_quads, types.WEST, 1, quad_shape, create_quads=True)
        # grow to the right
        if target_geometry[0] + target_geometry[2] > pos_x + self.shape[1] * quad_shape[1]:
            right_space = abs(target_geometry[0] + target_geometry[2] - (pos_x + self.shape[1] * quad_shape[1]))
            if right_space > 0:
                extra_quads = np.math.ceil(right_space / quad_shape[1])
                self.grow(extra_quads, types.EAST, 1, quad_shape, create_quads=True)
        # grow to the top
        if target_geometry[1] < pos_y:
            top_space = abs(target_geometry[1] - pos_y)
            if top_space > 0:
                extra_quads = np.math.ceil(top_space / quad_shape[0])
                self.grow(extra_quads, types.NORTH, 1, quad_shape, create_quads=True)
        # grow to the bottom
        if target_geometry[1] + target_geometry[3] > pos_y + self.shape[0] * quad_shape[0]:
            bot_space = abs(target_geometry[1] + target_geometry[3] - (pos_y + self.shape[0] * quad_shape[0]))
            if bot_space > 0:
                extra_quads = np.math.ceil(bot_space / quad_shape[0])
                self.grow(extra_quads, types.SOUTH, 1, quad_shape, create_quads=True)

    def __getitem__(self, item) -> np.ndarray:
        return self.data[item]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __repr__(self):
        return f"Quad(id={id(self)})"


if __name__ == '__main__':
    q = Quad(None, (2, 2), Quad)
    q.grow(2, types.NORTH, 1, (10, 10), True)
    #print(q.data)
    q.grow(2, types.EAST, 1, (10, 10), True)
    print(q.data)