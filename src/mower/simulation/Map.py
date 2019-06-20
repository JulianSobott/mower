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

    def update_rendering(self, passed_time):
        super().update()
        pass

    def draw(self, painter):
        qi = QtGui.QImage(self.data.data, self.size[0], self.size[1], QtGui.QImage.Format_Indexed8)
        qi.setColorTable(self.color_table)
        painter.drawImage(0, 0, qi)
        self.pix_map = QtGui.QPixmap.fromImage(qi)
        #painter.drawPixmap(0, 0, self.pix_map)

    def set_draw_map(self, allow):
        self.allow_draw_map = allow

    def mousePressEvent(self, mouse_event):
        pass

    def mouseMoveEvent(self, mouse_event):
        local_pos = mouse_event.localPos()
        if self.last_pos:
            # TODO: weighted solution
            # Lines are better because they ignore too fast mouse movement
            rr, cc, val = skimage.draw.line_aa(int(self.last_pos.y()), int(self.last_pos.x()), int(local_pos.y()),
                                               int(local_pos.x()))
            self.data[rr, cc] = val * 255
        else:
            stroke_width = 8
            self.data[int(local_pos.y()) - stroke_width//2: int(local_pos.y()) + stroke_width//2,
                        int(local_pos.x()) - stroke_width // 2: int(local_pos.x()) + stroke_width // 2] = 255
        self.last_pos = local_pos

    def mouseReleaseEvent(self, mouse_event):
        pass
