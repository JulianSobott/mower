"""
@author: Julian
@brief: Window, that provide control for the simulation
@description:
"""
import time

from PyQt5 import QtWidgets
from PyQt5.QtCore import QRect

from mower.simulation.MainWindow import MainWindowInterface
from mower.simulation.Logging import logger


class ControlWindow(QtWidgets.QMainWindow):
    TITLE = "Mower simulation CONTROL"
    SIZE = QRect(1030, 50, 500, 600)

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
        self.cb_run.setChecked(True)
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

        self.lbl_mouse_local = QtWidgets.QLabel("Local: ", self)
        self.lbl_mouse_local.move(20, 100)

        self.lbl_mouse_global = QtWidgets.QLabel("Global: ", self)
        self.lbl_mouse_global.move(20, 130)

    def update(self):
        self.update_fps()
        mouse_pos = self.main_window.map.last_local_pos
        if mouse_pos:
            self.lbl_mouse_local.setText(f"Local: {mouse_pos.x()}, {mouse_pos.y()}")
            global_mouse = self.main_window.map.transformation.inverted()[0].map(mouse_pos)
            self.lbl_mouse_global.setText(f"Global: {global_mouse.x()}, {global_mouse.y()}")

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


