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
from mower import simulation

__all__ = ["LocalWindowInterface"]


class LocalWindow(simulation.BaseWindow):
    """Window with all the information, that the mower has.

    Data:
    - local map
    """
    TITLE = "Local Window"
    SIZE = 0, 50, 500, 600

    def __init__(self):
        super().__init__()
        self.mower = simulation.Mower()
        #self.local_map: simulation.Map = self.mower.local_map
        #self.local_map.items.append(self.mower)
        #self.items.append(self.local_map)
        #self.event_receivers.append(self.local_map)


class LocalWindowInterface(simulation.BaseWindowInterface):

    def __init__(self):
        super().__init__(LocalWindow())
        self._control_window = None
