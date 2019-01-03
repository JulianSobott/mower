import sys

from PyQt5 import QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import QRect


UPDATE_INTERVAL = 500   # in milliseconds


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
        self.setWindowTitle(self.TITLE)
        self.setGeometry(self.SIZE)
        self.show()

    def update(self):
        print("update")



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
    # controlWindow = ControlWindow()
    sys.exit(app.exec())


if __name__=='__main__':
    init()
