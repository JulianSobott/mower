"""
@author: Julian
@brief: Window, that provide control for the simulation
@description:
"""
from PyQt5 import QtWidgets
from PyQt5.QtCore import QRect

from .MainWindow import MainWindowInterface


class ControlWindow(QtWidgets.QMainWindow):
    TITLE = "Mower simulation CONTROL"
    SIZE = QRect(600, 100, 500, 600)

    def __init__(self, main_window: MainWindowInterface):
        super().__init__(parent=None)

        self.setWindowTitle(self.TITLE)
        self.setGeometry(self.SIZE)

        self.main_window = main_window
        self._init_ui()
        self.show()

    def _init_ui(self):
        cb = QtWidgets.QCheckBox('Show title', self)
        cb.move(20, 20)
        cb.toggle()
        cb.stateChanged.connect(self.change_title)

    def change_title(self):
        self.setWindowTitle("New Title")
