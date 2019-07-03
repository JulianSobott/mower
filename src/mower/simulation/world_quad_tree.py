"""
:module: mower.
:synopsis:
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
import random
from typing import Optional, List
import numpy as np

from PyQt5 import QtGui

from mower.simulation.Painting import Painter, Renderable
from mower.simulation.Logging import logger


class Quad(Renderable):
    #: height, width
    SHAPE = (500, 500)
    neighbor_positions = [(-SHAPE[1], -SHAPE[0]),  # -1, -1
                          (0, -SHAPE[0]),  # 0, -1
                          (SHAPE[1], -SHAPE[0]),  # 1, -1

                          (-SHAPE[1], 0),
                          (0, 0),
                          (SHAPE[1], 0),

                          (-SHAPE[1], SHAPE[0]),
                          (0, SHAPE[0]),
                          (SHAPE[1], SHAPE[0]),
                          ]
    neighbor_indices = [(-1, -1), (0, -1), (1, -1),
                        (-1, 0), (0, 0), (1, 0),
                        (-1, 1), (0, 1), (1, 1)]

    def __init__(self, value: int, rel_pos=(0, 0)):
        self.neighbors: List[Optional[Quad]] = [None] * 9
        self.data = np.full((self.SHAPE[0], self.SHAPE[1]), value, np.uint8, 'C')
        self._locally_rendered = False
        self.rel_pos = rel_pos

    def render(self, painter: Painter, position, max_bounds, color_table):
        """

        :param painter:
        :param position: x, y
        :param max_bounds: min_x, min_y, max_x, max_y
        :param color_table:
        :return:
        """
        if (position[0] + self.SHAPE[1] > max_bounds[0] and  # left
                position[0] <= max_bounds[2] and  # right
                position[1] + self.SHAPE[0] > max_bounds[1] and  # top
                position[1] <= max_bounds[3]):  # bot

            if not self._locally_rendered:
                qi = QtGui.QImage(self.data.data, self.SHAPE[1], self.SHAPE[0], QtGui.QImage.Format_Indexed8)
                qi.setColorTable(color_table)
                # painter.drawImage(0, 0, qi)
                pix_map = QtGui.QPixmap.fromImage(qi)
                painter.drawPixmap(position[0], position[1], pix_map)
                self._locally_rendered = True

            for i, neighbor in enumerate(self.neighbors):
                if neighbor is not None and not neighbor._locally_rendered:
                    neighbor.render(painter,
                                    (position[0] + self.neighbor_positions[i][0],
                                     position[0] + self.neighbor_positions[i][1]),
                                    max_bounds,
                                    color_table)

        self._locally_rendered = False

    def add_neighbor(self, neighbor: 'Quad', pos_idx: int):
        """

        :param neighbor:
        :param pos_idx: Top: 0, 1, 2, Mid: 3, 5 Bot: 6, 7, 8
        :return:
        """
        # pos_translation = {0: 8, 1: 7, 2: 6, 3: 5, }
        self.neighbors[pos_idx] = neighbor
        neighbor.neighbors[8 - pos_idx] = self
        # TODO: add neighbor to all surrounding quads
        logger.debug("Added neighbor")

    def add_neighbors_to_fill(self, position, target_geometry, init_value: int):
        """

        :param position: x, y
        :param target_geometry: x, y, width, height
        :param init_value:
        :return:
        """
        if (target_geometry[0] <= position[0] <= target_geometry[0] + target_geometry[2] and
                target_geometry[1] <= position[1] <= target_geometry[1] + target_geometry[3]):
            for i, n in enumerate(self.neighbors):
                if n is None and i != 4:
                    if (target_geometry[0] <= position[0] + self.neighbor_positions[i][0] < target_geometry[0] +
                            target_geometry[2] and
                            target_geometry[1] <= position[1] + self.neighbor_positions[i][1] < target_geometry[1] +
                            target_geometry[3]):
                        self.add_neighbor(Quad(random.randint(0, 4), (self.rel_pos[0] + self.neighbor_indices[i][0],
                                                                      self.rel_pos[1] + self.neighbor_indices[i][1])),
                                          i)
                        self.neighbors[i].add_neighbors_to_fill((position[0] + self.neighbor_positions[i][0],
                                                                 position[1] + self.neighbor_positions[i][1]),
                                                                target_geometry, init_value)

    def surround_with_neighbours(self, init_value: int):
        for i, neighbor in enumerate(self.neighbors):
            if neighbor is None and i != 4:
                self.neighbors[i] = Quad(init_value, (self.rel_pos[0] + self.neighbor_indices[i][0],
                                                      self.rel_pos[1] + self.neighbor_indices[i][1]))

    def __repr__(self):
        return f"Quad({self.rel_pos})"
