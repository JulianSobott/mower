"""
@author: Julian
@brief: Window, that shows the graphical simulation
@description:
There is an extra class MainWindowInterface to encapsulate the Qt functionality.
This way only relevant/public functions are in MainWindowInterface.
MainWindowInterface is also useful to document functions.
"""
import time

from PyQt5 import QtWidgets
from PyQt5.QtCore import QRect
from PyQt5 import QtGui

from .Painting import Painter
from utils import Singleton
from .Mower import Mower
from .Map import Map
from .Logging import logger


__all__ = ["MainWindowInterface"]


class MainWindow(QtWidgets.QMainWindow):
    """Window responsible for rendering the simulation and calling the update function"""
    TITLE = "Mower simulation"
    SIZE = QRect(0, 0, 500, 600)

    def __init__(self):
        super().__init__(parent=None)

        self.items = []
        self.items.append(Map())
        self.items.append(Mower())

        self.last_update = time.time()

        self.setWindowTitle(self.TITLE)
        self.setGeometry(self.SIZE)
        self.show()

    def paintEvent(self, e):
        """Overridden from super()"""
        self._draw_widgets()

    def update_items(self):
        time_passed = time.time() - self.last_update
        for item in self.items:
            item.update_rendering(time_passed)
        self.repaint()

    def _draw_widgets(self):
        with Painter(self) as painter:
            painter.setPen(QtGui.QColor(200, 0, 0))
            for item in self.items:
                item.draw(painter)


class MainWindowInterface(metaclass=Singleton):
    """Class that communicates with MainWindow. contains all public functions"""
    def __init__(self):
        self._main_window = MainWindow()
        self._m_control_window = None
        self._m_is_paused = True

    def update(self):
        """Update all items and repaints the window"""
        self._m_control_window.update()
        if not self._m_is_paused:
            self._main_window.update_items()

    def pause(self):
        self._m_is_paused = True

    def resume(self):
        self._m_is_paused = False

    def toggle_pause(self):
        self._m_is_paused = not self._m_is_paused

    def set_control_window(self, control_window):
        self._m_control_window = control_window

