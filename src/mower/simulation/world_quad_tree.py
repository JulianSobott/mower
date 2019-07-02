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
from typing import Optional
import numpy as np

from PyQt5 import QtGui

from mower.simulation.Painting import Painter, Renderable


class Quad(Renderable):

    #: height, width
    SHAPE = (100, 100)

    def __init__(self, value: int):

        self.top_left: Optional[Quad] = None
        self.bot_left: Optional[Quad] = None
        self.top_right: Optional[Quad] = None
        self.bot_right: Optional[Quad] = None
        self.is_leaf = True
        self.value = value  #np.full((self.SHAPE[0], self.SHAPE[1]), value, np.uint8, 'C')

    def render(self, painter: Painter, geometry, max_depth: int, current_depth: int, color_table):
        """

        :param painter:
        :param geometry: x, y, width, height
        :param max_depth:
        :param current_depth:
        :param color_table:
        :return:
        """
        if max_depth == current_depth or self.is_leaf:
            avg_value = self.average_val()
            data = np.full((geometry[3], geometry[2]), avg_value, np.uint8, 'C')
            qi = QtGui.QImage(data.data, geometry[3], geometry[2], QtGui.QImage.Format_Indexed8)
            qi.setColorTable(color_table)
            painter.drawImage(0, 0, qi)
            pix_map = QtGui.QPixmap.fromImage(qi)
            #painter.drawPixmap(geometry[0], geometry[1], pix_map)
        else:
            self.top_left.render(painter,
                                 (geometry[0], geometry[1], geometry[2]/2, geometry[3]/2),
                                 max_depth, current_depth + 1, color_table)
            self.bot_left.render(painter,
                                 (geometry[0], geometry[1] + geometry[3] / 2, geometry[2] / 2, geometry[3] / 2),
                                 max_depth, current_depth + 1, color_table)
            self.top_right.render(painter,
                                  (geometry[0] + geometry[2] / 2, geometry[1], geometry[2] / 2, geometry[3] / 2),
                                  max_depth, current_depth + 1, color_table)
            self.bot_right.render(painter,
                                  (geometry[0] + geometry[2] / 2, geometry[1] + geometry[3] / 2,
                                   geometry[2] / 2, geometry[3] / 2),
                                  max_depth, current_depth + 1, color_table)

    def average_val(self) -> int:
        if self.is_leaf:
            return self.value
        else:
            return (self.top_left.average_val() + self.bot_left.average_val() + self.top_right.average_val() +
                    self.bot_right.average_val()) // 4


class WorldQuadTree:

    def __init__(self):
        self.root = Quad(1)

    def render(self, painter: Painter, geometry, max_depth: int, color_table):
        self.root.render(painter, geometry, max_depth, 0, color_table)
