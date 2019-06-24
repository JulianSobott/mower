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
import skimage.draw

from mower import core
from mower.simulation.Logging import logger
from mower.simulation.Painting import Renderable
from mower import simulation


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

    def __init__(self, items: List[Renderable] = []):
        """

        :param items: A list of all items that are rendered with transformations on the map.
        """
        super().__init__()
        super(core.Map, self).__init__()

        self.pix_map = QtGui.QPixmap(self.size[0].pixel(), self.size[1].pixel())
        self.items = items

        self.cells = np.zeros((self.shape[1], self.shape[0]))
        self.cells = np.reshape(self.cells, (self.shape[1], self.shape[0]))
        self.cells = np.require(self.cells, np.uint8, 'C')

        self.allow_draw_map = True

        self.last_local_pos = None
        # Position relative to window (All transformations are ignored and must be mapped)
        self.zoom = 1
        self.zoom_factor = 0.1

        self.transformation = QtGui.QTransform()
        self.mouse_move_mode = "DRAW"   # TRANSLATE

    def update_rendering(self, passed_time):
        super().update()
        for item in self.items:
            item.update_rendering(passed_time)

    def draw(self, painter):
        qi = QtGui.QImage(self.cells.data, self.shape[0], self.shape[1], QtGui.QImage.Format_Indexed8)
        qi.setColorTable(self.color_table)
        # painter.drawImage(0, 0, qi)
        self.pix_map = QtGui.QPixmap.fromImage(qi)
        painter.setTransform(self.transformation, combine=True)
        painter.drawPixmap(0, 0, self.pix_map)
        for item in self.items:
            item.draw(painter)

    def set_draw_map(self, allow):
        self.allow_draw_map = allow

    def mousePressEvent(self, mouse_event: QtGui.QMouseEvent):
        if mouse_event.button() == 1:
            # left
            self.mouse_move_mode = "DRAW"
        elif mouse_event.button() == 2:
            # right
            self.mouse_move_mode = "TRANSLATE"

        self.last_local_pos = mouse_event.localPos()

    def mouseMoveEvent(self, mouse_event):
        local_pos: QtCore.QPoint = mouse_event.localPos().toPoint()

        global_pos: QtCore.QPoint = self.transformation.inverted()[0].map(local_pos)
        last_global_pos: QtCore.QPoint = self.transformation.inverted()[0].map(self.last_local_pos)

        if self.mouse_move_mode == "DRAW":
            stroke_width = 20   # TODO: add parameters to ControlWindow (Color/Type, stroke_width, )
            try:

                self.add_line_data((last_global_pos.x(), last_global_pos.y()),
                                   (global_pos.x(), global_pos.y()),
                                   stroke_width,
                                   self.cells,
                                   self.OBSTACLE_COLOR)
            except IndexError:
                pass    # Drawing outside the window
        else:
            delta = global_pos - last_global_pos
            self.transformation.translate(delta.x(), delta.y())
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