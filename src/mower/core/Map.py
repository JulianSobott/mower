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
import numpy as np
import enum

from mower.core.Logging import logger
from mower.utils import Length


class CellType(enum.Enum):

    UNDEFINED = 0
    GRASS = 1
    OBSTACLE = 2


class Map:

    #: How big is a cell in the real world. The smaller the value the more precise is the map, but also the bigger it
    #: gets (memory).
    CELL_SIZE = Length(1000, Length.CENTIMETER)

    def __init__(self):

        #: The actual size in the real world
        self.size = (Length(50, Length.METER), Length(50, Length.METER))

        #: The array shape, based on CELL_SIZE
        self.shape = int((self.size[0] / self.CELL_SIZE).pixel()), int((self.size[1] / self.CELL_SIZE).pixel())

        #: The cell type for every cell
        self.cells = np.zeros(self.shape)

    def __getitem__(self, index):
        return self.cells[index]
