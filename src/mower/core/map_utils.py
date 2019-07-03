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
from typing import Union

import numpy as np


class Quad:

    def __init__(self, init_value, shape, data_type=int, parent: 'Quad' = None):
        self.parent: Quad = parent

        #: rows, cols or Height, Width
        self.shape = shape

        #: can contain either an array with other quads or primitive data
        self.data = np.full(shape, init_value, dtype=data_type)

        #: True: data contains primitives, False: data contains Quads
        self.is_leaf = True

    def value_at(self, x: int, y: int) -> Union[int, 'Quad']:
        """

        :param x:
        :param y:
        :return:
        """
        return self.data[y][x]

    def __getitem__(self, item) -> np.ndarray:
        return self.data[item]

    def __setitem__(self, key, value):
        self.data[key] = value
