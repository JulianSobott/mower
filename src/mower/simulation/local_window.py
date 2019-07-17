"""
:module: mower.simulation.local_window
:synopsis: Window with all the information, that the mower has.
:author: Julian Sobott
:author: 

public classes
-----------------

.. autoclass:: LocalWindowInterface
    :members:

private classes
-----------------

.. autoclass:: LocalWindow
    :members:


"""
from mower import simulation, core

__all__ = ["LocalWindowInterface"]


class LocalWindow(simulation.BaseWindow):
    """Window with all the information, that the mower has.

    Data:
    - local map
    """
    TITLE = "Local Window"
    SIZE = 0, 50, 500, 600

    def __init__(self, mower: simulation.Mower):
        super().__init__()
        self.mower = mower
        self.local_map: simulation.Map = self.mower.local_map
        self.local_map.items.append(self.mower)
        self.items.append(self.local_map)
        self.event_receivers.append(self.local_map)

        self.show()


class LocalWindowInterface(simulation.BaseWindowInterface):

    def __init__(self, mower: simulation.Mower):
        super().__init__(LocalWindow(mower))
        self._control_window = None

    def set_pen_cell_type(self, new_type: core.CellType):
        self._window.local_map.pen_cell_type = new_type

    def set_pen_drawing_mode(self, new_mode: 'simulation.DrawingMode'):
        self._window.local_map.pen_drawing_mode = new_mode


