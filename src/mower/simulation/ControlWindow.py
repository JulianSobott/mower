"""
@author: Julian
@brief: Window, that provide control for the simulation
@description:
"""
import time

from PyQt5 import QtWidgets, QtCore

from mower.simulation import BaseWindow
from mower.simulation.Logging import logger
from mower.simulation.global_window import GlobalWindowInterface
from mower.simulation.local_window import LocalWindowInterface


class ControlWindow(BaseWindow):
    TITLE = "Mower simulation CONTROL"
    SIZE = (1030, 50, 500, 600)

    def __init__(self, local_window: LocalWindowInterface, global_window: GlobalWindowInterface):
        super().__init__()
        self.last_shown = 0
        self.local_window = local_window
        self.global_window = global_window
        self._init_ui()
        self.show()

    def _init_ui(self):
        self.cb_run = QtWidgets.QCheckBox('Run', self)
        self.cb_run.move(20, 20)
        self.cb_run.setChecked(True)
        if self.cb_run.isChecked():
            self.local_window.resume()
            self.global_window.resume()
        else:
            self.local_window.pause()
            self.global_window.pause()

        self.cb_run.stateChanged.connect(self.local_window.toggle_pause)
        self.cb_run.stateChanged.connect(self.global_window.toggle_pause)

        self.lbl_fps = QtWidgets.QLabel("FPS: ", self)
        self.lbl_fps.move(20, 40)

        btn_draw_map = QtWidgets.QPushButton(self)
        btn_draw_map.setText("Draw map")
        btn_draw_map.move(20, 70)
        btn_draw_map.clicked.connect(self._click_draw_map)

        self.lbl_simulation_speed = QtWidgets.QLabel("Simulation speed: 1.0", self)
        self.lbl_simulation_speed.setGeometry(20, 110, 230, 10)
        slider_simulation_speed = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        slider_simulation_speed.setSliderPosition(50)
        slider_simulation_speed.sliderMoved.connect(self._slider_simulation_speed_update)
        slider_simulation_speed.move(300, 110)

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
        # self.global_window.set_draw_map(True)

    def _slider_simulation_speed_update(self, value: int):
        """
        0: speed = 0
        50: speed = 1
        100 speed = 2
        :param value: [0 - 100] 0: slowest (stop), 100: fastest
        :return:
        """
        self._set_simulation_speed(value/50)

    def _set_simulation_speed(self, time_scale: float):
        self.local_window.set_time_scale(time_scale)
        self.global_window.set_time_scale(time_scale)
        self.lbl_simulation_speed.setText(f"Simulation speed: {time_scale}")
