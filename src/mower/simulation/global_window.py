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
from mower import simulation

__all__ = ["GlobalWindowInterface"]


class GlobalWindow(simulation.BaseWindow):
    """Window that shows all data. This is also data that is only available in simulation.

    Data:
    - global map
    - mower position

    """
    TITLE = "Global Window"
    SIZE = 510, 50, 500, 600

    def __init__(self, mower: simulation.Mower):
        super().__init__()
        self.mower = mower
        self.global_map = simulation.Map([self.mower])
        self.items.append(self.global_map)
        self.event_receivers.append(self.global_map)

        self.show()


class GlobalWindowInterface(simulation.BaseWindowInterface):

    def __init__(self, mower: simulation.Mower):
        super().__init__(GlobalWindow(mower))
        self._control_window = None
