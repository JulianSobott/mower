"""
@author: Julian
@brief:
@description:
"""
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtCore import QRect

from .Logging import logger
import Core
from .Painting import Renderable
from .Painting import Painter


class Map(Core.Map, Renderable):
    GRASS_COLOR = QtGui.QColor(0, 180, 0)
    CELL_OUTLINE_COLOR = QtGui.QColor(0, 0, 0)

    def __init__(self):
        super().__init__()
        for x in range(100):
            for y in range(100):
                self.cells.append(Core.GrasslandCell(x, y))
        self.pix_map = QtGui.QPixmap(1000, 1000)
        self.f_update_pix_map = True

    def update_rendering(self, passed_time):
        super().update()
        pass

    def draw(self, painter):
        if self.f_update_pix_map:
            self.f_update_pix_map = False
            self.update_pix_map()
            painter.drawPixmap(0, 0, self.pix_map)
        else:
            painter.drawPixmap(0, 0, self.pix_map)

    def update_pix_map(self):
        with Painter(self.pix_map) as pain:
            self.pix_map.fill(QtCore.Qt.gray)
            for cell in self.cells:
                rect = QRect((cell.x * cell.SIZE).pixel(), (cell.y * cell.SIZE).pixel(),
                             cell.SIZE.pixel(), cell.SIZE.pixel())
                pain.fillRect(rect, QtGui.QBrush(self.GRASS_COLOR, QtCore.Qt.SolidPattern))
                pain.setPen(self.CELL_OUTLINE_COLOR)
                pain.drawRect(rect)
