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

    def __init__(self, items: List[Renderable] = ()):
        """

        :param items: A list of all items that are rendered with transformations on the map.
        """
        super(core.Map, self).__init__()
        self.size = (800, 1000)
        self.pix_map = QtGui.QPixmap(self.size[0], self.size[1])
        self.items = items

        self.data = np.zeros((self.size[1], self.size[0]))
        self.data = np.reshape(self.data, (self.size[1], self.size[0]))
        self.data = np.require(self.data, np.uint8, 'C')

        self.allow_draw_map = True

        self.last_local_pos = None
        # Position relative to window (All transformations are ignored and must be mapped)
        self.zoom = 1
        self.zoom_factor = 0.1

        self.transformation = QtGui.QTransform()
        self.mouse_move_mode = "DRAW"   # TRANSLATE

    def update_rendering(self, passed_time):
        super().update()
        pass

    def draw(self, painter):
        qi = QtGui.QImage(self.data.data, self.size[0], self.size[1], QtGui.QImage.Format_Indexed8)
        qi.setColorTable(self.color_table)
        # painter.drawImage(0, 0, qi)
        self.pix_map = QtGui.QPixmap.fromImage(qi)
        painter.setTransform(self.transformation)
        painter.drawPixmap(0, 0, self.pix_map)

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
        local_pos = mouse_event.localPos()

        global_pos = self.transformation.inverted()[0].map(local_pos)
        last_global_pos = self.transformation.inverted()[0].map(self.last_local_pos)

        if self.mouse_move_mode == "DRAW":
            stroke_width = 20   # TODO: add parameters to ControlWindow (Color/Type, stroke_width, )
            try:
                self.draw_thick_line(last_global_pos, global_pos, stroke_width, self.data, self.OBSTACLE_COLOR)
            except IndexError:
                pass    # Drawing outside the window
        else:
            delta = global_pos - last_global_pos
            self.transformation.translate(delta.x(), delta.y())
        self.last_local_pos = local_pos

    @staticmethod
    def draw_thick_line(pos1: QtCore.QPoint, pos2: QtCore.QPoint, thickness: int, data: np.array, color_idx=0):
        # TODO: find way that ensures, that line is always thick enough (take angular in account)
        poly = np.array((
            (int(pos1.y() + thickness//2), int(pos1.x() + thickness//2)),
            (int(pos2.y() + thickness//2), int(pos2.x() + thickness//2)),
            (int(pos2.y() - thickness // 2), int(pos2.x() - thickness // 2)),
            (int(pos1.y() - thickness // 2), int(pos1.x() - thickness // 2)),
        ))
        rr, cc = skimage.draw.polygon(poly[:, 0], poly[:, 1])
        data[rr, cc] = color_idx

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