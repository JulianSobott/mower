"""
@author: Julian
@brief: Window, that provide control for the simulation
@description:
"""
import time

from PyQt5 import QtWidgets
from PyQt5.QtCore import QRect

from .MainWindow import MainWindowInterface
from .Logging import logger


class ControlWindow(QtWidgets.QMainWindow):
    TITLE = "Mower simulation CONTROL"
    SIZE = QRect(600, 100, 500, 600)

    def __init__(self, main_window: MainWindowInterface):
        super().__init__(parent=None)

        self.setWindowTitle(self.TITLE)
        self.setGeometry(self.SIZE)

        self.last_update = time.time()
        self.last_shown = 0

        self.main_window = main_window
        self._init_ui()
        self.show()

    def _init_ui(self):
        self.cb_run = QtWidgets.QCheckBox('Run', self)
        self.cb_run.move(20, 20)
        self.cb_run.setChecked(False)
        if self.cb_run.isChecked():
            self.main_window.resume()
        else:
            self.main_window.pause()
        self.cb_run.stateChanged.connect(self.main_window.toggle_pause)

        self.lbl_fps = QtWidgets.QLabel("FPS: ", self)
        self.lbl_fps.move(20, 40)

        btn_draw_map = QtWidgets.QPushButton(self)
        btn_draw_map.setText("Draw map")
        btn_draw_map.move(20, 70)
        btn_draw_map.clicked.connect(self._click_draw_map)

    def update(self):
        self.update_fps()

    def update_fps(self):
        curr_time = time.time()
        time_diff = curr_time - self.last_update
        self.last_update = curr_time
        if curr_time - self.last_shown > 1:
            fps = 1/time_diff
            self.lbl_fps.setText("FPS: " + str(fps))
            self.last_shown = curr_time

    def _click_draw_map(self):
        self.cb_run.setChecked(False)
        self.main_window.set_draw_map(True)


