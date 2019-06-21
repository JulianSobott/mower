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
            if self.last_local_pos:
                # TODO: weighted solution
                # Lines are better because they ignore too fast mouse movement
                # for i in range(1, 100, 10):
                #     rr, cc = skimage.draw.line(int(last_global_pos.y() + i), int(last_global_pos.x() + i),
                #                                int(global_pos.y()+ i),
                #                                        int(global_pos.x() + i))
                #     self.data[rr, cc] = 255 // (i/10)
                # poly = np.array((
                #     (30, 200),
                #     (50, 210),
                #     (90, 90),
                #     (70, 70),
                # ))
                # #rr, cc = skimage.draw.polygon(poly[:, 0], poly[:, 1])

                self.draw_thick_line(last_global_pos, global_pos, 10, self.data)
            else:
                stroke_width = 8
                self.data[int(global_pos.y()) - stroke_width//2: int(global_pos.y()) + stroke_width//2,
                            int(global_pos.x()) - stroke_width // 2: int(global_pos.x()) + stroke_width // 2] = 255

        else:
            delta = global_pos - last_global_pos
            self.transformation.translate(delta.x(), delta.y())
        self.last_local_pos = local_pos

    @staticmethod
    def draw_thick_line(pos1: QtCore.QPoint, pos2: QtCore.QPoint, thickness: int, data: np.array):
        # TODO: find way that ensures, that line is always thick enough (take angular in account)
        poly = np.array((
            (int(pos1.y() + thickness//2), int(pos1.x() + thickness//2)),
            (int(pos2.y() + thickness//2), int(pos2.x() + thickness//2)),
            (int(pos2.y() - thickness // 2), int(pos2.x() - thickness // 2)),
            (int(pos1.y() - thickness // 2), int(pos1.x() - thickness // 2)),
        ))
        rr, cc = skimage.draw.polygon(poly[:, 0], poly[:, 1])
        data[rr, cc] = 255

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