"""
@author: Julian
@brief: Window, that provide control for the simulation
@description:
"""
import functools
import time

from PyQt5 import QtWidgets, QtCore, QtGui

import mower.core.map_utils
from mower import core, simulation, utils
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

        btn_restart = QtWidgets.QPushButton("Restart", self)
        btn_restart.move(60, 20)
        btn_restart.clicked.connect(self._restart)

        self.lbl_fps = QtWidgets.QLabel("FPS: ", self)
        self.lbl_fps.move(20, 40)

        self.lbl_simulation_speed = QtWidgets.QLabel("Simulation speed: 1.0", self)
        self.lbl_simulation_speed.setGeometry(20, 110, 230, 10)
        slider_simulation_speed = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        slider_simulation_speed.setSliderPosition(50)
        slider_simulation_speed.sliderMoved.connect(self._slider_simulation_speed_update)
        slider_simulation_speed.move(300, 110)

        lbl_drawing_header = QtWidgets.QLabel("Drawing:", self)
        lbl_drawing_header.setFont(QtGui.QFont("Times", 14, QtGui.QFont.Bold))
        lbl_drawing_header.move(20, 130)

        grp_cell_type = QtWidgets.QGroupBox("Cell Type", self)
        rb_grass = QtWidgets.QRadioButton("Grass", self)
        rb_grass.clicked.connect(functools.partial(self._update_drawing_cell_type, mower.core.map_utils.CellType.GRASS))
        rb_obstacle = QtWidgets.QRadioButton("Obstacle", self)
        rb_obstacle.clicked.connect(functools.partial(self._update_drawing_cell_type, mower.core.map_utils.CellType.OBSTACLE))
        rb_undefined = QtWidgets.QRadioButton("Undefined", self)
        rb_undefined.clicked.connect(functools.partial(self._update_drawing_cell_type, mower.core.map_utils.CellType.UNDEFINED))

        rb_obstacle.setChecked(True)  # Default value in simulation.Map

        vbox_cell_type = QtWidgets.QVBoxLayout()
        vbox_cell_type.addWidget(rb_grass)
        vbox_cell_type.addWidget(rb_obstacle)
        vbox_cell_type.addWidget(rb_undefined)
        vbox_cell_type.addStretch(1)
        grp_cell_type.setLayout(vbox_cell_type)
        grp_cell_type.setGeometry(20, 170, 100, 100)

        grp_pen_drawing_mode = QtWidgets.QGroupBox("Cell Type", self)
        rb_free_hand = QtWidgets.QRadioButton("Free hand", self)
        rb_free_hand.clicked.connect(functools.partial(self._update_pen_drawing_mode, simulation.DrawingMode.FREE_HAND))
        rb_rectangle = QtWidgets.QRadioButton("Rectangle", self)
        rb_rectangle.clicked.connect(functools.partial(self._update_pen_drawing_mode, simulation.DrawingMode.RECTANGLE))
        rb_line = QtWidgets.QRadioButton("Line", self)
        rb_line.setEnabled(False)
        rb_line.clicked.connect(functools.partial(self._update_pen_drawing_mode, simulation.DrawingMode.LINE))
        rb_oval = QtWidgets.QRadioButton("Oval", self)
        rb_oval.clicked.connect(functools.partial(self._update_pen_drawing_mode, simulation.DrawingMode.OVAL))
        rb_oval.setEnabled(False)

        rb_rectangle.setChecked(True)  # Default value in simulation.Map

        vbox_cell_type = QtWidgets.QVBoxLayout()
        vbox_cell_type.addWidget(rb_free_hand)
        vbox_cell_type.addWidget(rb_rectangle)
        vbox_cell_type.addWidget(rb_line)
        vbox_cell_type.addWidget(rb_oval)
        vbox_cell_type.addStretch(1)
        grp_pen_drawing_mode.setLayout(vbox_cell_type)
        grp_pen_drawing_mode.setGeometry(120, 170, 100, 100)

        btn_save = QtWidgets.QPushButton("Save", self)
        btn_save.move(20, 290)
        btn_save.clicked.connect(self._save_data)

        btn_save = QtWidgets.QPushButton("Load", self)
        btn_save.move(200, 290)
        btn_save.clicked.connect(self._load_data)

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

    def _update_drawing_cell_type(self, new_type: mower.core.map_utils.CellType):
        self.local_window.set_pen_cell_type(new_type)
        self.global_window.set_pen_cell_type(new_type)

    def _update_pen_drawing_mode(self, new_mode: 'simulation.DrawingMode'):
        self.local_window.set_pen_drawing_mode(new_mode)
        self.global_window.set_pen_drawing_mode(new_mode)

    def _restart(self):
        self.local_window.restart()
        self.global_window.restart()

    def _save_data(self):
        utils.data_storage.save_data(self.global_window.map, self.global_window.mower)

    def _load_data(self):
        full_name = "SAVE_19_07_18_19_44_55"    # TODO: Add widget in window
        utils.data_storage.load_data(self.global_window.map, self.global_window.mower, full_name)
