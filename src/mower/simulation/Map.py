"""
@author: Julian
@brief:
@description:
"""
from typing import List

from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
import numpy as np

from mower import core
from mower.core.map_utils import Quad
from mower.simulation.Logging import logger
from mower.simulation.Painting import Renderable
from mower.utils import types


class Map(core.Map, Renderable, QtWidgets.QWidget):
    BACKGROUND_COLOR = 0
    GRASS_COLOR = 1
    OBSTACLE_COLOR = 2
    CELL_OUTLINE_COLOR = 3

    color_table = [
        QtGui.qRgb(100, 100, 100),
        QtGui.qRgb(0, 255, 0),
        QtGui.qRgb(100, 50, 0),
        QtGui.qRgb(0, 0, 0)
    ]

    def __init__(self, items: List[Renderable] = None, is_global: bool = False):
        """

        :param items: A list of all items that are rendered with transformations on the map.
        :param is_global: Defines if the map represents the global view of the scene or the local.
        """
        super().__init__()
        super(core.Map, self).__init__()

        if items is None:
            self.items = []
        else:
            self.items = items

        #: True: The global positions will be taken for rendering
        #: False: The local positions (core.mower) will be taken for rendering
        self.is_global = is_global

        self.window_size = QtCore.QPoint(500, 600)

        self.allow_draw_map = True

        #: Position relative to window (All transformations are ignored and must be mapped)
        self.last_local_pos = None

        self.zoom = 1
        self.zoom_factor = 0.1

        #: x, y, width, height
        self.max_bounds = [0, 0, self.window_size.x(), self.window_size.y()]
        self.root_quad.grow_to_size(self.max_bounds)

        self.map_offset = [0, 0]

        self.transformation = QtGui.QTransform()
        self.mouse_move_mode = "DRAW"  # TRANSLATE

    def update_rendering(self, passed_time):
        super().update()
        for item in self.items:
            item.update_rendering(passed_time)

    def draw(self, painter, *args):
        painter.setTransform(self.transformation, combine=True)
        for row in range(self.root_quad.shape[0]):
            for col in range(self.root_quad.shape[1]):
                quad: Quad = self.root_quad[row][col]
                pos_x = (-self.root_quad.offset[0] + col) * quad.shape[1]
                pos_y = (-self.root_quad.offset[1] + row) * quad.shape[0]
                if (quad is not None and
                        self.max_bounds[0] <= pos_x + quad.shape[1] and pos_x <= self.max_bounds[2] and
                        self.max_bounds[1] <= pos_y + quad.shape[0] and pos_y <= self.max_bounds[3]):
                    self.draw_quad(painter, quad, pos_x, pos_y)
        for item in self.items:
            item.draw(painter, self.is_global)

    def set_draw_map(self, allow):
        self.allow_draw_map = allow

    def mousePressEvent(self, mouse_event: QtGui.QMouseEvent):
        if mouse_event.button() == 1:
            # left
            self.mouse_move_mode = "DRAW"
        elif mouse_event.button() == 2:
            # right
            self.mouse_move_mode = "TRANSLATE"

        self.last_local_pos = mouse_event.localPos().toPoint()

    def mouseMoveEvent(self, mouse_event):
        local_pos: QtCore.QPoint = mouse_event.localPos().toPoint()

        global_pos: QtCore.QPoint = self.transformation.inverted()[0].map(local_pos)
        last_global_pos: QtCore.QPoint = self.transformation.inverted()[0].map(self.last_local_pos)

        if self.mouse_move_mode == "DRAW":
            stroke_width = 10  # TODO: add parameters to ControlWindow (Color/Type, stroke_width, )
            try:

                self.add_line_data((last_global_pos.x(), last_global_pos.y()),
                                   (global_pos.x(), global_pos.y()),
                                   stroke_width,
                                   self.cells,
                                   self.OBSTACLE_COLOR)
                # logger.debug(f"{global_pos}")
                # logger.debug(f"{self.index2pos(global_pos.x(), global_pos.y())}")
                # logger.debug(f"{self.pos2index(*self.index2pos(global_pos.x(), global_pos.y()))}")
            except IndexError:
                pass  # Drawing outside the window
        else:
            delta = global_pos - last_global_pos
            self.transformation.translate(delta.x(), delta.y())
            self.updated_transformation()
        self.last_local_pos = local_pos

    def mouseReleaseEvent(self, mouse_event):
        self.last_local_pos = None

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

    def cell_type_at(self, x: types.Length, y: types.Length):
        row, col = self.pos2index(x, y)
        return core.CellType.by_value(self.cells[row][col])

    def draw_quad(self, painter, quad: Quad, x, y):
        qi = QtGui.QImage(quad.data, quad.shape[1], quad.shape[0], QtGui.QImage.Format_Indexed8)
        qi.setColorTable(self.color_table)
        painter.drawImage(x, y, qi)
        # pix_map = QtGui.QPixmap.fromImage(qi)
        # painter.drawPixmap(x, y, pix_map)

    def updated_transformation(self):
        minimum: QtCore.QPoint = self.transformation.inverted()[0].map(QtCore.QPoint(0, 0))
        maximum: QtCore.QPoint = self.transformation.inverted()[0].map(self.window_size)
        self.max_bounds[0] = minimum.x()
        self.max_bounds[1] = minimum.y()
        self.max_bounds[2] = maximum.x()
        self.max_bounds[3] = maximum.y()

        self.root_quad.grow_to_size(self.max_bounds)
