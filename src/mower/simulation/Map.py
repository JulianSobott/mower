"""
@author: Julian
@brief:
@description:
"""
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import QRect
import numpy as np
import skimage.draw

from mower.core import Map as CoreMap
from mower.simulation.Logging import logger
from mower.simulation.Painting import Renderable
from mower.simulation.Painting import Painter


class Map(CoreMap.Map, Renderable, QtWidgets.QWidget):
    GRASS_COLOR = QtGui.QColor(0, 180, 0)
    CELL_OUTLINE_COLOR = QtGui.QColor(0, 0, 0)

    def __init__(self):
        super().__init__()
        self.size = (1000, 1000)
        self.pix_map = QtGui.QPixmap(1000, 1000)

        self.data = np.random.rand(self.size[0]*self.size[1])*255
        self.data = np.reshape(self.data, (self.size[1], self.size[0]))

        self.data = np.zeros((1000, 1000))
        self.data = np.reshape(self.data, (self.size[1], self.size[0]))
        #self.data[0:100][0:100] = 255
        self.data = np.require(self.data, np.uint8, 'C')

        self.color_table = []
        for i in range(256):
            self.color_table.append(QtGui.qRgb(i, i/2, 1))

        self.allow_draw_map = True
        self.last_pos = None
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

        self.last_pos = mouse_event.localPos()

    def mouseMoveEvent(self, mouse_event):
        local_pos = mouse_event.localPos()
        # TODO: proper translation into global space
        global_pos = self.transformation.map(local_pos)
        #logger.debug(local_pos)
        #logger.debug(global_pos)

        if self.mouse_move_mode == "DRAW":
            if self.last_pos:
                # TODO: weighted solution
                # Lines are better because they ignore too fast mouse movement
                rr, cc, val = skimage.draw.line_aa(int(self.last_pos.y()), int(self.last_pos.x()), int(global_pos.y()),
                                                   int(global_pos.x()))
                self.data[rr, cc] = val * 255
            else:
                stroke_width = 8
                self.data[int(global_pos.y()) - stroke_width//2: int(global_pos.y()) + stroke_width//2,
                            int(global_pos.x()) - stroke_width // 2: int(global_pos.x()) + stroke_width // 2] = 255

        else:
            logger.debug(self.last_pos)
            delta = local_pos - self.last_pos
            logger.debug(delta)
            self.transformation.translate(delta.x(), delta.y())
        self.last_pos = local_pos

    def mouseReleaseEvent(self, mouse_event):
        self.last_pos = None

    def wheelEvent(self, event: QtGui.QWheelEvent):
        num_degree = event.angleDelta().y()
        if num_degree > 0:
            scale_delta = self.zoom_factor
            self.zoom += self.zoom_factor
        else:
            scale_delta = -self.zoom_factor
            self.zoom -= self.zoom_factor
        self.transformation.scale(1 + scale_delta, 1 + scale_delta)