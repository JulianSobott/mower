"""
:module: mower.core.map_utils
:synopsis: Classes and functions for the map
:author: Julian Sobott
:author: 


public classes
-----------------

.. autoclass:: Quad
    :members:
    :undoc-members:

.. autoclass:: CellType
    :members:
    :undoc-members:

"""
import enum
from typing import Union, Type, Tuple

import numpy as np

from mower.utils import types
from mower.core.Logging import logger

#: HEIGHT, WIDTH
DATA_SHAPE = (500, 500)


class Quad:
    """
    A Quad is part of the map. The map is build up from quads that are placed grid wise. A Quad can either contain
    other quads store in an 2d array or if it is a leaf it contains data stored inside an integer array.
    """

    SURROUND_WITH_BORDER = True  # just for debugging

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
        self.is_leaf = data_type is np.uint8

    def get_value_at(self, x: int, y: int) -> int:
        """

        :param x: position
        :param y: position
        :return:
        """
        if self.is_leaf:
            return self.data[y][x]
        else:
            x_idx = x // DATA_SHAPE[1] + self.offset[0]
            y_idx = y // DATA_SHAPE[0] + self.offset[1]
            return self.data[y_idx][x_idx].get_value_at(x % DATA_SHAPE[1], y % DATA_SHAPE[0])

    def set_value_at(self, x: int, y: int, value: int) -> None:
        if self.is_leaf:
            self.data[y][x] = value
        else:
            x_idx = x // DATA_SHAPE[1] + self.offset[0]
            y_idx = y // DATA_SHAPE[0] + self.offset[1]
            self.data[y_idx][x_idx].set_value_at(x % DATA_SHAPE[1], y % DATA_SHAPE[0], value)

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

    def set_data_by_array(self, array: np.ndarray, x: int, y: int):
        """

        :param array: numpy integer array filled with the new data
        :param x: position on the map. Can be negative
        :param y: position on the map. Can be negative
        :return:
        """
        if self.is_leaf:
            self.data[y:y + array.shape[0], x:x + array.shape[1]] = array
        else:
            curr_y = y
            array_idx_y = 0

            while array_idx_y < array.shape[0]:
                curr_x = x
                array_idx_x = 0
                height = 0
                while array_idx_x < array.shape[1]:
                    (quad_idx_y, quad_idx_x), (data_idx_y, data_idx_x) = self._pos_to_indices(curr_x, curr_y)
                    width = min((-self.offset[0] * DATA_SHAPE[1] + (quad_idx_x + 1) * DATA_SHAPE[1]) - curr_x,
                                array.shape[1] - array_idx_x)
                    height = min((-self.offset[1] * DATA_SHAPE[0] + (quad_idx_y + 1) * DATA_SHAPE[0]) - curr_y,
                                 array.shape[0] - array_idx_y)

                    quad_array = array[array_idx_y:array_idx_y + height,
                                       array_idx_x:array_idx_x + width]
                    self.data[quad_idx_y][quad_idx_x].set_data_by_array(quad_array, data_idx_x, data_idx_y)
                    curr_x += width
                    array_idx_x += width
                curr_y += height
                array_idx_y += height

    def set_data_by_indices(self, rows: np.ndarray, cols: np.ndarray, values: Union[int, np.ndarray]):
        """

        :param rows: numpy array of y positions
        :param cols: numpy array of x positions (matching thr y positions)
        :param values:
        :return:
        """
        if self.is_leaf:
            self.data[rows, cols] = values
        else:
            while len(rows) > 0 and len(cols) > 0:
                curr_row = rows[0]
                curr_col = cols[0]
                (quad_idx_y, quad_idx_x), (data_idx_y, data_idx_x) = self._pos_to_indices(curr_col, curr_row)
                map_indices = []
                for i in range(len(rows)):
                    if ((-self.offset[1] * DATA_SHAPE[0]) + quad_idx_y * DATA_SHAPE[0] <= rows[i] < (
                            -self.offset[1] * DATA_SHAPE[0]) + (quad_idx_y + 1) * DATA_SHAPE[0]) and (
                            (-self.offset[0] * DATA_SHAPE[1]) + quad_idx_x * DATA_SHAPE[1] <= cols[i] < (
                            -self.offset[0] * DATA_SHAPE[1]) + (quad_idx_x + 1) * DATA_SHAPE[1]):
                        map_indices.append(i)

                map_rows = rows[map_indices]
                map_cols = cols[map_indices]
                rows = np.delete(rows, map_indices)
                cols = np.delete(cols, map_indices)

                quad_rows = map_rows - (quad_idx_y - self.offset[1]) * DATA_SHAPE[0]
                quad_cols = map_cols - (quad_idx_x - self.offset[0]) * DATA_SHAPE[1]
                if isinstance(values, int):
                    quad_values = values
                else:
                    quad_values = values[quad_rows, quad_cols]

                self.data[quad_idx_y][quad_idx_x].set_data_by_indices(quad_rows, quad_cols, quad_values)
            assert len(rows) == 0 and len(cols) == 0, f"Rows {len(rows)} and cols {cols} must be same size"

    def grow_grass_cells(self):
        """Increases the value of every grass cell by one"""
        if self.is_leaf:
            self.data[(CellType.MIN_GRASS.value <= self.data) & (self.data < CellType.MAX_GRASS.value)] += 1
        else:
            for row in self.data:
                for quad in row:
                    quad.grow_grass_cells()

    def get_array_at(self, x: int, y: int, width: int, height: int) -> np.ndarray:
        """

        :param x: position
        :param y: position
        :param width:
        :param height:
        :return: An Array filled with the data of a rectangle area with geometry: x, y, width, height
        """
        if self.is_leaf:
            return self.data[y: y + height, x: x + width]
        else:
            curr_y = y
            array_idx_y = 0

            ret_array = np.zeros((height, width), dtype=np.uint8)

            while array_idx_y < height:
                curr_x = x
                array_idx_x = 0
                quad_height = 0
                while array_idx_x < width:
                    (quad_idx_y, quad_idx_x), (data_idx_y, data_idx_x) = self._pos_to_indices(curr_x, curr_y)
                    quad_width = min((-self.offset[0] * DATA_SHAPE[1] + (quad_idx_x + 1) * DATA_SHAPE[1]) - curr_x,
                                     width - array_idx_x)
                    quad_height = min((-self.offset[1] * DATA_SHAPE[0] + (quad_idx_y + 1) * DATA_SHAPE[0]) - curr_y,
                                      height - array_idx_y)

                    quad_array = self.data[quad_idx_y][quad_idx_x].get_array_at(data_idx_x, data_idx_y,
                                                                                quad_width, quad_height)
                    logger.debug(curr_y + quad_height)
                    ret_array[array_idx_y:array_idx_y + quad_height, array_idx_x: array_idx_x + quad_width] = quad_array
                    curr_x += quad_width
                    array_idx_x += quad_width
                curr_y += quad_height
                array_idx_y += quad_height
            return ret_array

    def _pos_to_indices(self, x: int, y: int) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """

        :param x: position
        :param y: position
        :return: ((quad_idx_y, quad_idx_x), (data_idx_y, data_idx_x))
        """
        quad_idx_x = x // DATA_SHAPE[1] + self.offset[0]
        quad_idx_y = y // DATA_SHAPE[0] + self.offset[1]
        data_idx_x = x % DATA_SHAPE[1]
        data_idx_y = y % DATA_SHAPE[0]
        return (quad_idx_y, quad_idx_x), (data_idx_y, data_idx_x)

    def __getitem__(self, item) -> np.ndarray:
        return self.data[item]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __repr__(self):
        return f"Quad(id={id(self)})"


class CellType(enum.Enum):

    UNDEFINED = 0
    GRASS = 20
    OBSTACLE = 2
    MIN_GRASS = 20
    MAX_GRASS = 40

    @classmethod
    def _init(cls):
        cls._values = {0: cls.UNDEFINED, 1: cls.GRASS, 2: cls.OBSTACLE,
                       **{i: cls.GRASS for i in range(cls.MIN_GRASS.value, cls.MAX_GRASS.value + 1)}}

    @classmethod
    def by_value(cls, val):
        return cls._values[val]

CellType._init()
