import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer


from .MainWindow import MainWindowInterface
from .ControlWindow import ControlWindow


UPDATE_INTERVAL = 10    # in milliseconds (10^=60fps ?)


def setup_windows():
    """All object must be stored in an object to prevent garbage collection"""
    app = QtWidgets.QApplication(sys.argv)

    main_window = MainWindowInterface()
    control_window = ControlWindow(main_window)
    main_loop = setup_main_loop(main_window)
    sys.exit(app.exec())


def setup_main_loop(main_window):
    """timer must be returned and saved to prevent garbage collection"""
    timer = QTimer()
    timer.timeout.connect(main_window.update)
    timer.start(UPDATE_INTERVAL)
    return timer


if __name__ == '__main__':
    setup_windows()
