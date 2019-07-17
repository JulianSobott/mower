"""
:module: mower.simulation.global_window
:synopsis: Window that show all global information. Information that are only available in simulation
:author: Julian Sobott
:author:

public classes
-----------------

.. autoclass:: GlobalWindowInterface
    :members:

private classes
-----------------

.. autoclass:: GlobalWindow
    :members:


"""
import mower.core.map_utils
from mower import simulation, core

__all__ = ["GlobalWindowInterface"]


class GlobalWindow(simulation.BaseWindow):
    """Window that shows all data. This is also data that is only available in simulation.

    Data:
    - global map
    - mower position

    """
    TITLE = "Global Window"
    SIZE = 510, 50, 500, 600

    def __init__(self, mower_obj: simulation.Mower):
        super().__init__()
        self.mower = mower_obj
        self.global_map = simulation.Map([self.mower], is_global=True)
        self.items.append(self.global_map)
        self.event_receivers.append(self.global_map)

        self.show()

    @property
    def map(self):
        return self.global_map

    def restart(self):
        self.global_map.reset()


class GlobalWindowInterface(simulation.BaseWindowInterface):

    def __init__(self, mower_obj: simulation.Mower):
        super().__init__(GlobalWindow(mower_obj))
        self._control_window = None

    @property
    def map(self):
        self._window: GlobalWindow
        return self._window.map

    def set_pen_cell_type(self, new_type: mower.core.map_utils.CellType):
        self._window.global_map.pen_cell_type = new_type

    def set_pen_drawing_mode(self, new_mode: 'simulation.DrawingMode'):
        self._window.global_map.pen_drawing_mode = new_mode

    def restart(self):
        self._window.restart()
