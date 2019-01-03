import sys
import random

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QRect
from PyQt5 import QtCore
from PyQt5 import QtGui

from Painting import Painter


UPDATE_INTERVAL = 10    # in milliseconds (10^=60fps ?)


class Window(QtWidgets.QMainWindow):
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setFixedSize(500, 600)
        self.show()


class MainWindow(QtWidgets.QMainWindow):
    TITLE = "Mower simulation"
    SIZE = QRect(0, 0, 500, 600)

    def __init__(self):
        super().__init__(parent=None)

        self.x_value = 0
        self.y_value = 10

        self.setWindowTitle(self.TITLE)
        self.setGeometry(self.SIZE)
        self.show()

    def paintEvent(self, e):
        self.draw_widgets()

    def update(self):
        self.x_value += 1
        self.repaint()

    def draw_widgets(self):
        with Painter(self) as painter:
            painter.setPen(QtCore.Qt.red)
            painter.drawLine(self.x_value, 40, 250, 40)


class ControlWindow(QtWidgets.QMainWindow):
    TITLE = "Mower simulation CONTROL"
    SIZE = QRect(600, 100, 500, 600)

    def __init__(self):
        super().__init__(parent=None)

        self.setWindowTitle(self.TITLE)
        self.setGeometry(self.SIZE)

        cb = QtWidgets.QCheckBox('Show title', self)
        cb.move(20, 20)
        cb.toggle()
        #cb.stateChanged.connect(self.changeTitle)

        self.show()


def init():
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    timer = QTimer()
    timer.timeout.connect(mainWindow.update)
    timer.start(UPDATE_INTERVAL)
    controlWindow = ControlWindow()
    sys.exit(app.exec())


if __name__=='__main__':
    init()
