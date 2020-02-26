"""
:module: mower.simulation.Map
:synopsis: Class that extends the :class:`mower.core.Map.Map` to render it and allows editing it
:author: Julian Sobott
:author:

public classes
-----------------

.. autoclass:: Map
    :members:
    :undoc-members:

.. autoclass:: DrawingMode
    :members:
    :undoc-members:

private classes
-----------------

.. autoclass:: Shape
    :members:
    :undoc-members:

.. autoclass:: Rectangle
    :members:
    :undoc-members:
    :show-inheritance:


"""
from abc import ABC
from typing import List, Union
import enum

from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
import numpy as np

import mower.core.map_utils
from mower import core
from mower.core.map_utils import Quad
from mower.simulation import paths
from mower.simulation.Logging import logger
from mower.simulation.Painting import Renderable, Painter
from mower.utils import types


class Map(Renderable, QtWidgets.QWidget):

    color_table = (
            [
                QtGui.qRgb(100, 100, 100),  # UNDEFINED
                QtGui.qRgb(0, 255, 0),  # GRASS
                QtGui.qRgb(100, 50, 0),  # OBSTACLE

            ]
            # filler
            + [QtGui.qRgb(0, 0, 0) for i in range(3, mower.core.map_utils.CellType.MIN_GRASS.value)]

            # GRASS Heights 20: short - 40: high
            + [QtGui.qRgb(0, i * 3 + 50, 0) for i in range(mower.core.map_utils.CellType.MIN_GRASS.value,
                                                           mower.core.map_utils.CellType.MAX_GRASS.value + 1)])

    def __init__(self, items: List[Renderable] = None, is_global: bool = False):
        """

        :param items: A list of all items that are rendered with transformations on the map.
        :param is_global: Defines if the map represents the global view of the scene or the local.
        """
        super().__init__()
        self.map_data = core.Map()

        # debug
        # self.map_data.debug_add_rect(10, 10, 100, 100)

        if items is None:
            self.items = []
        else:
            self.items = items

        #: True: The global positions will be taken for rendering
        #: False: The local positions (core.mower) will be taken for rendering
        self.is_global = is_global

        self.window_size = QtCore.QPoint(500, 600)

        #: value of the cells that is set, when they are colored by drawing
        self.pen_cell_type = mower.core.map_utils.CellType.OBSTACLE
        self.pen_drawing_mode = DrawingMode.RECTANGLE
        self.temp_drawing_shape: Union[None, Shape] = None

        #: Position relative to window (All transformations are ignored and must be mapped)
        self.last_local_pos = None

        self.zoom = 1
        self.zoom_factor = 0.1

        #: x, y, width, height
        self.max_bounds = [0, 0, self.window_size.x(), self.window_size.y()]

        self.transformation = QtGui.QTransform()
        self.mouse_move_mode = "DRAW"  # TRANSLATE

        #: Debug image
        self._debug_grid_img = QtGui.QImage(paths.get_asset_path("grid_transparent.png"))
        self._debug_render_grid = True

    def update_rendering(self, passed_time):
        self.map_data.update(passed_time)
        for item in self.items:
            item.update_rendering(passed_time)

    def draw(self, painter, *args):
        painter.setTransform(self.transformation, combine=True)

        painter.setBrush(QtGui.QBrush(QtGui.QColor(Map.color_table[self.pen_cell_type.value])))
        painter.setPen(QtGui.QColor(255, 180, 0))
        for path_data in self.map_data.paths:
            path = QtGui.QPainterPath()
            start = path_data.begin.pos.x, path_data.begin.pos.y
            path.moveTo(*start)
            for node in path_data:
                painter.drawEllipse(node.pos.x - 2, node.pos.y - 2, 4, 4)
                path.lineTo(node.pos.x, node.pos.y)
            path.lineTo(*start)
            painter.drawPath(path)

        if self.temp_drawing_shape is not None:
            self.temp_drawing_shape.draw(painter)

        # for item in self.items:
        #     item.draw(painter, self.is_global)

    def mousePressEvent(self, mouse_event: QtGui.QMouseEvent):
        self.last_local_pos = mouse_event.localPos().toPoint()

        if mouse_event.button() == 1:
            # left
            self.mouse_move_mode = "DRAW"
            global_pos: QtCore.QPoint = self.transformation.inverted()[0].map(self.last_local_pos)

            if self.pen_drawing_mode == DrawingMode.RECTANGLE:
                self.map_data.begin_dynamic_rect(global_pos.x(), global_pos.y())
            elif self.pen_drawing_mode == DrawingMode.FREE_HAND:
                self.map_data.begin_new_path()
                self.map_data.add_point(global_pos.x(), global_pos.y())
        elif mouse_event.button() == 2:
            # right
            self.mouse_move_mode = "TRANSLATE"

    def mouseMoveEvent(self, mouse_event):
        local_pos: QtCore.QPoint = mouse_event.localPos().toPoint()

        global_pos: QtCore.QPoint = self.transformation.inverted()[0].map(local_pos)
        last_global_pos: QtCore.QPoint = self.transformation.inverted()[0].map(self.last_local_pos)

        if self.mouse_move_mode == "DRAW":

            if self.pen_drawing_mode == DrawingMode.FREE_HAND:
                self.map_data.add_point(global_pos.x(), global_pos.y())
            elif self.pen_drawing_mode == DrawingMode.RECTANGLE:
                self.map_data.update_dynamic_rect(global_pos.x(), global_pos.y())

        else:
            delta = global_pos - last_global_pos
            self.transformation.translate(delta.x(), delta.y())
            self.updated_transformation()
        self.last_local_pos = local_pos

    def mouseReleaseEvent(self, mouse_event):
        self.last_local_pos = None
        if self.mouse_move_mode == "DRAW":
            self.map_data.end_new_path()
        if self.temp_drawing_shape is not None:
            self.temp_drawing_shape = None

    def wheelEvent(self, event: QtGui.QWheelEvent):
        num_degree = event.angleDelta().y()
        if num_degree > 0:
            scale_delta = self.zoom_factor
            self.zoom += self.zoom_factor
        else:
            scale_delta = -self.zoom_factor
            self.zoom -= self.zoom_factor
        self.transformation.scale(1 + scale_delta, 1 + scale_delta)
        self.updated_transformation()

    def updated_transformation(self):
        minimum: QtCore.QPoint = self.transformation.inverted()[0].map(QtCore.QPoint(0, 0))
        maximum: QtCore.QPoint = self.transformation.inverted()[0].map(self.window_size)
        self.max_bounds[0] = minimum.x()
        self.max_bounds[1] = minimum.y()
        self.max_bounds[2] = maximum.x()
        self.max_bounds[3] = maximum.y()

    def reset(self):
        """

        :return:
        """
        self.__init__(self.items, self.is_global)


class DrawingMode(enum.IntEnum):
    FREE_HAND = 0
    RECTANGLE = 1
    LINE = 2
    OVAL = 3


class Shape(Renderable, ABC):

    def __init__(self, cell_type: mower.core.map_utils.CellType):
        self.cell_type = cell_type

    def get_array_data(self):
        raise NotImplementedError

    def update_geometry_by_point(self, x: int, y: int):
        raise NotImplementedError


class Rectangle(Shape):

    def __init__(self, cell_type: mower.core.map_utils.CellType, x: int, y: int, width: int, height: int):
        super().__init__(cell_type)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, painter: Painter, *args):
        painter.fillRect(self.x, self.y, self.width, self.height, QtGui.QColor(Map.color_table[self.cell_type.value]))

    def update_rendering(self, passed_time):
        pass

    def update_geometry_by_point(self, x: int, y: int):
        self.width = x - self.x
        self.height = y - self.y

    def get_array_data(self):
        self.normalize_geometry()
        arr = np.full((self.height, self.width), self.cell_type.value, dtype=np.uint8)
        return arr, self.x, self.y

    def normalize_geometry(self):
        if self.height < 0:
            self.y += self.height
            self.height *= -1
        if self.width < 0:
            self.x += self.width
            self.width *= -1

    def __repr__(self):
        return f"Quad({self.x}, {self.y}, {self.width}, {self.height})"
