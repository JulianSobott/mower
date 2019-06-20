import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer


from mower.simulation.MainWindow import MainWindowInterface
from mower.simulation.ControlWindow import ControlWindow
from mower.simulation.Logging import logger


UPDATE_INTERVAL = 10    # in milliseconds (10^=60fps ?)


def setup_windows():
    """All object must be stored in an object to prevent garbage collection"""
    app = QtWidgets.QApplication(sys.argv)

    main_window = MainWindowInterface()
    control_window = ControlWindow(main_window)
    main_window.set_control_window(control_window)
    main_loop = setup_main_loop(main_window)
    logger.debug("Start simulation")
    sys.exit(app.exec())


def setup_main_loop(main_window):
    """timer must be returned and saved to prevent garbage collection"""
    timer = QTimer()
    timer.timeout.connect(main_window.update)
    timer.start(UPDATE_INTERVAL)
    return timer


if __name__ == '__main__':
    setup_windows()
