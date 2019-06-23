import sys
from typing import List

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer

from mower import simulation
from mower.simulation.MainWindow import MainWindowInterface
from mower.simulation.ControlWindow import ControlWindow
from mower.simulation.Logging import logger
from mower.simulation.global_window import GlobalWindowInterface
from mower.simulation.local_window import LocalWindowInterface

UPDATE_INTERVAL = 10    # in milliseconds (10^=60fps ?)


def setup_windows():
    """All object must be stored in an object to prevent garbage collection"""
    app = QtWidgets.QApplication(sys.argv)

    global_window = GlobalWindowInterface()
    local_window = LocalWindowInterface()
    main_window = MainWindowInterface()
    control_window = ControlWindow(local_window, global_window)
    global_window.set_control_window(control_window)
    local_window.set_control_window(control_window)
    main_loop = setup_main_loop([local_window, global_window])
    logger.debug("Start simulation")
    sys.exit(app.exec())


def setup_main_loop(windows: List[simulation.BaseWindowInterface]):
    """timer must be returned and saved to prevent garbage collection"""
    timer = QTimer()
    for window in windows:
        timer.timeout.connect(window.update)
    timer.start(UPDATE_INTERVAL)
    return timer


if __name__ == '__main__':
    setup_windows()
