import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QRect
from PyQt5 import QtGui

from Source.Simulation.Painting import Painter, Mower


UPDATE_INTERVAL = 10    # in milliseconds (10^=60fps ?)


class MainWindow(QtWidgets.QMainWindow):
    """Window responsible for rendering the simulation and calling the update function"""
    TITLE = "Mower simulation"
    SIZE = QRect(0, 0, 500, 600)

    def __init__(self):
        super().__init__(parent=None)

        self.items = []
        self.items.append(Mower())

        self.setWindowTitle(self.TITLE)
        self.setGeometry(self.SIZE)
        self.show()

    def paintEvent(self, e):
        self.draw_widgets()

    def update(self):
        for item in self.items:
            item.update()
        self.repaint()

    def draw_widgets(self):
        with Painter(self) as painter:
            painter.setPen(QtGui.QColor(200, 0, 0))
            for item in self.items:
                item.draw(painter)


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
        cb.stateChanged.connect(self.change_title)

        self.show()

    def change_title(self):
        self.setWindowTitle("New Title")


def start():
    app = QtWidgets.QApplication(sys.argv)

    main_window = MainWindow()
    control_window = ControlWindow()

    timer = QTimer()
    timer.timeout.connect(main_window.update)
    timer.start(UPDATE_INTERVAL)

    sys.exit(app.exec())


if __name__ == '__main__':
    start()
