"""
:module: mower.simulation.base_window
:synopsis: Base window with basic functionality and settings
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
import time
from typing import List
import traceback

from PyQt5 import QtWidgets, QtCore

from mower.simulation.Painting import Renderable, Painter
from mower.utils import Singleton


class EventReceiverWidget:
    """Events that can be fired by the GUI. More Events can be added here and then also in the BaseWindow."""

    def mousePressEvent(self, mouse_event):
        pass

    def mouseMoveEvent(self, mouse_event):
        pass

    def mouseReleaseEvent(self, mouse_event):
        pass

    def wheelEvent(self, wheel_event):
        pass


class BaseWindow(QtWidgets.QMainWindow, EventReceiverWidget):

    TITLE = "set Title in inherited class"
    SIZE = (0, 0, 500, 600)

    def __init__(self):
        super().__init__(parent=None)

        self.event_receivers: List[EventReceiverWidget] = []
        self.items: List[Renderable] = []
        self.last_update = time.time()
        self.setWindowTitle(self.TITLE)
        self.setGeometry(QtCore.QRect(*self.SIZE))
        self.is_paused = False

        #: Makes it possible to slow down or speed up the game without affecting the FPS.
        #: = 1: No effect
        #: < 1: slow down
        #: > 1: fasten
        self.time_scale = 1.

    def paintEvent(self, e):
        """Overridden from super()"""
        self._draw_items()

    def update_items(self):
        """Update all items. The time_passed is may be affected by a scale factor to slow down or fasten the
        simulation"""
        now = time.time()
        if self.is_paused:
            time_passed = 0
        else:
            time_passed = (now - self.last_update) * self.time_scale
        self.last_update = now
        for item in self.items:
            try:
                item.update_rendering(time_passed)
            except Exception as e:
                traceback.print_exc()
                raise e
        self.repaint()

    def _draw_items(self):
        with Painter(self) as painter:
            for item in self.items:
                item.draw(painter)

    def mousePressEvent(self, mouse_event):
        self.forward_event(self.mousePressEvent, mouse_event)

    def mouseMoveEvent(self, mouse_event):
        self.forward_event(self.mouseMoveEvent, mouse_event)

    def mouseReleaseEvent(self, mouse_event):
        self.forward_event(self.mouseReleaseEvent, mouse_event)

    def wheelEvent(self, wheel_event):
        self.forward_event(self.wheelEvent, wheel_event)

    def forward_event(self, function, event):
        for receiver in self.event_receivers:
            receiver.__getattribute__(function.__name__)(event)


class BaseWindowInterface(metaclass=Singleton):
    """Class that communicates with MainWindow. contains all public functions"""

    def __init__(self, window: BaseWindow):
        self._window: BaseWindow = window
        self._control_window = None

    def update(self):
        """Update all items and repaints the window"""
        self._control_window.update()
        self._window.update_items()

    def pause(self):
        self._window.is_paused = True

    def resume(self):
        self._window.is_paused = False

    def toggle_pause(self):
        self._window.is_paused = not self._window.is_paused

    def set_control_window(self, control_window):
        self._control_window = control_window

    def set_time_scale(self, time_scale: float):
        self._window.time_scale = time_scale
